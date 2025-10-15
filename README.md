# FinBot-MA
FinBot.ma is a web-based tool for Moroccan users, offering calculators for IR (Income Tax), IS (Corporate Tax), TVA (VAT), Loans, Investments, and Budgets. Built with HTML, CSS, &amp; JavaScript, it features a responsive design with EN-FR-AR support, generating graphs with Matplotlib. Data logs to Google Sheets via n8n, &amp; an AI chatbot assists users. 

# Step by Step How to Run the FinBot.ma Project :
Follow these steps to set up and run the FinBot.ma financial tools platform locally:


## 1) Clone the Repository:

Open a terminal and navigate to your desired directory.

Run: 
```
git clone https://github.com/btc3o/finbot-ma.git
```


This downloads the project files to a folder named finbot-ma.



## 2) Navigate to the Project Folder:

Change to the project directory (in your path): 
```
cd finbot-ma
```


## 3) Install Dependencies:

- Ensure Python 3.8+ is installed (python --version).
- Install required packages listed in requirements.txt:

Run: 
```
pip install -r requirements.txt
```

This installs Flask, Flask-CORS, Matplotlib, NumPy, and optional Arabic support libraries.



## 4) Set Up the Environment:

Ensure you have a local web server environment. No database is needed, but n8n webhooks (for Google Sheets logging) require a separate n8n instance (optional for basic use).



## 5) Run the Flask Backend:

Start the Flask server by running in your path of the folder of finbot-ma: 
```
python app.py
```

The server will run on http://localhost:5000. Check the terminal for confirmation (e.g., "Running on http://localhost:5000").



## 6) Open the Frontend:

Open finbot.html in a web browser (e.g., double-click the file or use file:///path/to/finbot-ma/finbot.html).




## 7) Interact with the Application:

Use the calculators (IR, IS, TVA, Loan, Investment, Budget) by entering values and clicking "Calculate."
Graphs will display for supported calculators, and data will log to n8n webhooks if configured.
Switch languages (English, French, Arabic) using the top-right buttons.
The AI chatbot (via Chatbase) will assist with queries.



## 8) Configure your google sheet:

to track users inputs & results etc, we gonna use google sheet for this, u gonna create a document in google sheet and name it: ##finbot-data , then u gonna create 6 sheets, like next:

## sheet1: 
(is calculator)

<img width="1315" height="593" alt="Capture d’écran (1938)" src="https://github.com/user-attachments/assets/49635f7c-2b18-4882-bfc1-6f261465d28c" />

## sheet2:
(ir calculator)

<img width="1312" height="491" alt="Capture d’écran (1944)" src="https://github.com/user-attachments/assets/f9e75849-42e9-4a23-997d-b5f882524547" />


## sheet3: 
(tva calculator)

<img width="1198" height="523" alt="Capture d’écran (1945)" src="https://github.com/user-attachments/assets/341c31f2-b64b-4ab4-8e8b-544b9f4d7ece" />


## sheet4:
(loan calculator)

<img width="1294" height="495" alt="Capture d’écran (1941)" src="https://github.com/user-attachments/assets/987ab7f2-ef6f-4e2e-9222-ac79f882c310" />


## sheet5:
(investment calculator)

<img width="1418" height="516" alt="Capture d’écran (1942)" src="https://github.com/user-attachments/assets/8d4c7668-c39b-4420-927c-29218bd4746c" />

## sheet6:
(budget calculator)

<img width="1212" height="525" alt="Capture d’écran (1943)" src="https://github.com/user-attachments/assets/bf28fffb-a72d-4917-9f1c-744eba1131a8" />





## 9) Configure your n8n workflow:

For easy setup create 6 webhooks (for our 6 sheets), if u have skills in n8n you can create just one webhook and use IF condition in the code, but in our case we will code a simple user friendly workflow, this is the final result workflow how it look like: 

<img width="1354" height="780" alt="Capture d’écran (1937)" src="https://github.com/user-attachments/assets/5c3629cd-c008-44ac-ae58-ce18a7a4508a" />

to create this exact final result, follow this step by step:

### 9.1) :

create 6 webhooks, for all of them choose "POST" http, leave everything else as its   

## 9.2) : 

for all webhooks, click on + button, search about "code" , choose code with JavaScript, then paste for each code field of each webhook this following javascript codes :

### JS code of webhook 1 :

```
// Code for the n8n Function (Code in JavaScript) node

// Get the webhook payload (it's an array, so grab the first item)
const data = $input.all()[0].json;

// Extract the 'body' array that holds your entries
const input = data.body || [];

// Map each entry into a row for Google Sheets
return input.map(entry => {
  return {
    json: {
      Type: entry.type,
      Revenue: entry.inputs?.revenue ?? null,
      Expenses: entry.inputs?.expenses ?? null,
      Result: entry.result ?? null,
      Language: entry.lang ?? null,
      IP: data.headers?.['x-real-ip'] ?? null,
      Timestamp: new Date().toISOString()
    }
  };
});
```

### JS Code for webhook 2 :

```
// Code for the n8n Function (Code in JavaScript) node

// Get the webhook payload (it's an array, so grab the first item)
const data = $input.all()[0].json;

// Extract the 'body' array that holds your entries
const input = data.body || [];

// Map each entry into a row for Google Sheets
return input.map(entry => {
  return {
    json: {
      Type: entry.type ?? "ir",
      "Annual Income (MAD)": entry.inputs?.annualIncome ?? null,
      Dependents: entry.inputs?.dependents ?? null,
      Result: entry.result ?? null,
      Language: entry.lang ?? null,
      IP: data.headers?.["x-real-ip"] ?? null,
      Timestamp: new Date().toISOString()
    }
  };
});
```

### JS code for webhook 3 :

```
// Code for the n8n Function (Code in JavaScript) node

// Get the webhook payload (it's an array, so grab the first item)
const data = $input.all()[0].json;

// Extract the 'body' array that holds your entries
const input = data.body || [];

// Map each entry into a row for Google Sheets
return input.map(entry => {
  return {
    json: {
      Type: entry.type,
      "Amount HT (MAD)": entry.inputs?.amount_ht ?? null,
      Rate: entry.inputs?.rate ?? null,
      Result: entry.result ?? null,
      Language: entry.lang ?? null,
      Timestamp: new Date().toISOString()
    }
  };
});
```

### JS code for webhook 4 : 

```
// Code for the n8n Function (Code in JavaScript) node

// Get the webhook payload (it's an array, so grab the first item)
const data = $input.all()[0].json;

// Extract the 'body' array that holds your entries
const input = data.body || [];

// Map each entry into a row for Google Sheets
return input.map(entry => {
  return {
    json: {
      Type: entry.type,
      "Loan Amount (MAD)": entry.inputs?.loan_amount ?? null,
      "Rate (%)": entry.inputs?.rate ?? null,
      "Duration (months)": entry.inputs?.duration ?? null,
      Language: entry.lang ?? null,
      Timestamp: new Date().toISOString()
    }
  };
});
```

### JS code for webhook 5 :

```
// Code for the n8n Function (Code in JavaScript) node

// Get the webhook payload (it's an array, so grab the first item)
const data = $input.all()[0].json;

// Extract the 'body' array that holds your entries
const input = data.body || [];

// Map each entry into a row for Google Sheets
return input.map(entry => {
  return {
    json: {
      Type: entry.type,
      "Initial Investment": entry.inputs?.initial_investment ?? null,
      "Rate (%)": entry.inputs?.rate ?? null,
      Years: entry.inputs?.years ?? null,
      "Monthly Contribution": entry.inputs?.monthly_contribution ?? null,
      Result: entry.result ?? null,
      Language: entry.lang ?? null,
      Timestamp: new Date().toISOString()
    }
  };
});
```

### JS code for webhook 6 :

```
// Code for the n8n Function (Code in JavaScript) node

// Get the webhook payload (it's an array, so grab the first item)
const data = $input.all()[0].json;

// Extract the 'body' array that holds your entries
const input = data.body || [];

// Map each entry into a row for Google Sheets
return input.map(entry => {
  return {
    json: {
      Type: entry.type,
      "Monthly Income": entry.inputs?.monthly_income ?? null,
      "Monthly Expenses": entry.inputs?.monthly_expenses ?? null,
      Result: entry.result ?? null,
      Language: entry.lang ?? null,
      Timestamp: new Date().toISOString()
    }
  };
});
```

## 9.3) :

after we done the JS codes setups, we will move to google sheet setup for each webhook, (this is explanation of webhook 1 & u will repeat it for other webhooks.) :

click on + button in front of each JS code ---)  connect to your google sheet account ---) then for webhook choose "finbot-data" from list of document & sheet1 from list of sheet (for next sheets choose sheet2 for 2nd webhook etc... sheet 6 for 6th webhook) ---) choose map each column manually ---) now in values to send here : 

<img width="583" height="766" alt="Capture d’écran (1947)" src="https://github.com/user-attachments/assets/d52e16a3-27ad-447e-9420-1f90355691cc" />

paste this following values for each sheet for each webhook :

for example
## sheet 1 (of webhook 1) :

### Type:
```
{{ $json.Type }}
```

### Revenue:
```
{{ $json.Revenue }}
```

### Expenses:
```
{{ $json.Expenses }}
```

### Result:
```
{{ $json.Result }}
```

### Language:
```
{{ $json.Language }}
```

### Timestamp:
```
{{ $json.Timestamp }}
```
-------------------------------
## sheet 2 (of webhook 2) :

### Type:
```
{{ $json.Type }}
```

### Annual Income (MAD) :
```
{{ $json['Annual Income (MAD)'] }}
```

### Dependents:
```
{{ $json.Dependents }}
```

### Result:
```
{{ $json.Result }}
```

### Language:
```
{{ $json.Language }}
```

### Timestamp:
```
{{ $json.Timestamp }}
```
-----------------------------
U will repeat same things for all other sheets in same way


## 10) : Your Webhook production URL configuration: 

after u done the google sheet setup of all 6 sheets, go to each webhook & get your production URL, make sure u saved your workflow!! as i if u refreshed u will lost all files, then open config-webhooks.html, and paste your webhook for each one, it will help u replace them directly in the html! and your html now will be 100% cool.

-------------------------------

Congrats! now you fully setup & u can use FinBot-MA how u want, (u can also modify the chatbase api to yours, & train it how u want with your data)


## 10) Troubleshooting:

If graphs don’t load, ensure Flask is running and input valid numbers (e.g., positive years for Investment).
Check the terminal for errors (e.g., "Graph generation failed").
For n8n integration, set up webhooks with the URLs in finbot.html (e.g., https://gg4444.app.n8n.cloud/webhook/...).



## 9) Stop the Server:

Press Ctrl+C in the terminal to stop the Flask server when done.



Enjoy using FinBot.ma!


## Notes:

Dependencies: Ensure all libraries from requirements.txt are installed.
Image: The person.png file is used for the bot illustration and should be in the same directory.
Optional n8n: For full functionality (data logging), configure n8n with the provided webhook URLs.
