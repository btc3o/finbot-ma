import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS

# New imports for Arabic support
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    print("Warning: arabic_reshaper and python-bidi not installed. Arabic text may not render correctly. Install with: pip install arabic-reshaper python-bidi")

app = Flask(__name__)
CORS(app)

translations = {
    'en': {
        'ylabel': 'Amount (MAD)',
        'ir_title': 'Income Tax Breakdown',
        'ir_categories': ['Gross Income', 'Tax Before Credit (20%)', 'Dependent Credit', 'Net Tax'],
        'is_title': 'Corporate Tax Breakdown',
        'is_categories': ['Revenue', 'Expenses', 'Profit', 'Corporate Tax (20%)'],
        'tva_title': 'VAT Breakdown (TTC: {ttc:.2f} MAD)',
        'tva_labels': ['Amount HT', 'TVA'],
        'loan_title': 'Loan Cost Breakdown (Monthly: {monthly_payment:.2f} MAD)',
        'loan_labels': ['Principal', 'Total Interest'],
        'invest_title': 'Investment Growth Over Time',
        'invest_xlabel': 'Years',
        'invest_ylabel': 'Value (MAD)',
        'budget_title': 'Budget Allocation (Income: {income:.2f} MAD)',
        'budget_labels': ['Expenses', 'Remaining'],
    },
    'fr': {
        'ylabel': 'Montant (MAD)',
        'ir_title': 'Décomposition de l\'impôt sur le revenu',
        'ir_categories': ['Revenu brut', 'Impôt avant crédit (20%)', 'Crédit pour personnes à charge', 'Impôt net'],
        'is_title': 'Décomposition de l\'impôt sur les sociétés',
        'is_categories': ['Revenu', 'Dépenses', 'Bénéfice', 'Impôt sur les sociétés (20%)'],
        'tva_title': 'Décomposition de la TVA (TTC: {ttc:.2f} MAD)',
        'tva_labels': ['Montant HT', 'TVA'],
        'loan_title': 'Décomposition des coûts du prêt (Mensuel: {monthly_payment:.2f} MAD)',
        'loan_labels': ['Principal', 'Intérêts totaux'],
        'invest_title': 'Croissance de l\'investissement au fil du temps',
        'invest_xlabel': 'Années',
        'invest_ylabel': 'Valeur (MAD)',
        'budget_title': 'Allocation du budget (Revenu: {income:.2f} MAD)',
        'budget_labels': ['Dépenses', 'Restant'],
    },
    'ar': {
        'ylabel': 'المبلغ (MAD)',
        'ir_title': 'تحليل الضريبة على الدخل',
        'ir_categories': ['الدخل الإجمالي', 'الضريبة قبل الائتمان (20%)', 'ائتمان المعالين', 'الضريبة الصافية'],
        'is_title': 'تحليل الضريبة على الشركات',
        'is_categories': ['الإيرادات', 'المصاريف', 'الربح', 'الضريبة على الشركات (20%)'],
        'tva_title': 'تحليل الضريبة على القيمة المضافة (TTC: {ttc:.2f} MAD)',
        'tva_labels': ['المبلغ بدون الضريبة', 'الضريبة على القيمة المضافة'],
        'loan_title': 'تحليل تكاليف القرض (شهري: {monthly_payment:.2f} MAD)',
        'loan_labels': ['الأصل', 'الفوائد الإجمالية'],
        'invest_title': 'نمو الاستثمار مع مرور الوقت',
        'invest_xlabel': 'السنوات',
        'invest_ylabel': 'القيمة (MAD)',
        'budget_title': 'تخصيص الميزانية (الدخل: {income:.2f} MAD)',
        'budget_labels': ['المصاريف', 'المتبقي'],
    }
}

def reshape_arabic(text, lang):
    if lang == 'ar' and ARABIC_SUPPORT:
        return get_display(arabic_reshaper.reshape(text))
    return text

@app.route('/api/graph', methods=['POST'])
def generate_graph():
    data = request.json
    calc_type = data['type']
    inputs = data['inputs']
    result = data['result']
    lang = data.get('lang', 'en')
    trans = translations.get(lang, translations['en'])

    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.style.use('seaborn-v0_8-whitegrid')  # Clean style

        if lang == 'ar':
            plt.rcParams['font.family'] = 'Amiri'  # Or 'DejaVu Sans' if Amiri not installed
            plt.rcParams['text.usetex'] = False
            plt.rcParams['axes.unicode_minus'] = False
            ax.invert_xaxis()  # Optional: Flip x-axis for better RTL flow

        if calc_type == 'ir':
            income = inputs['income']
            dependents = inputs['dependents']
            deduction = dependents * 500
            tax_before = income * 0.2
            net_tax = max(0, tax_before - deduction)
            
            categories = [reshape_arabic(cat, lang) for cat in trans['ir_categories']]
            values = [income, tax_before, deduction, net_tax]
            
            bars = ax.bar(categories, values, color=['#4CAF50', '#2196F3', '#FFC107', '#F44336'])
            ax.set_title(reshape_arabic(trans['ir_title'], lang), fontsize=16, fontweight='bold')
            ax.set_ylabel(reshape_arabic(trans['ylabel'], lang), fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', 
                        ha='center', va='bottom', fontsize=10)

        elif calc_type == 'is':
            revenue = inputs['revenue']
            expenses = inputs['expenses']
            profit = revenue - expenses
            tax = max(0, profit * 0.2)
            
            categories = [reshape_arabic(cat, lang) for cat in trans['is_categories']]
            values = [revenue, expenses, profit, tax]
            
            bars = ax.bar(categories, values, color=['#4CAF50', '#F44336', '#2196F3', '#FFC107'])
            ax.set_title(reshape_arabic(trans['is_title'], lang), fontsize=16, fontweight='bold')
            ax.set_ylabel(reshape_arabic(trans['ylabel'], lang), fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', 
                        ha='center', va='bottom', fontsize=10)

        elif calc_type == 'tva':
            ht = inputs['amountHT']
            rate = inputs['rate']
            tva = ht * rate
            ttc = ht + tva
            
            labels = [reshape_arabic(label, lang) for label in trans['tva_labels']]
            sizes = [ht, tva]
            colors = ['#4CAF50', '#2196F3']
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                   shadow=True, startangle=90, textprops={'fontsize': 12})
            ax.set_title(reshape_arabic(trans['tva_title'].format(ttc=ttc), lang), fontsize=16, fontweight='bold')
            ax.axis('equal')

        elif calc_type == 'loan':
            P = inputs['amount']
            annual_rate = inputs['rate']
            n = inputs['months']
            monthly_payment = result
            
            total_paid = monthly_payment * n
            total_interest = total_paid - P
            
            labels = [reshape_arabic(label, lang) for label in trans['loan_labels']]
            sizes = [P, total_interest]
            colors = ['#4CAF50', '#F44336']
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                   shadow=True, startangle=90, textprops={'fontsize': 12})
            ax.set_title(reshape_arabic(trans['loan_title'].format(monthly_payment=monthly_payment), lang), fontsize=16, fontweight='bold')
            ax.axis('equal')

        elif calc_type == 'invest':
            P = inputs['initial']
            annual_rate = inputs['rate']
            years = inputs['years']
            c = inputs['monthly']
            r = annual_rate / 100 / 12
            months = years * 12
            
            values = []
            current = P
            if years <= 0 or months <= 0:
                # Handle edge case: no growth
                values = [P]
                years_list = [0]
            else:
                for m in range(1, months + 1):
                    current = current * (1 + r) + c
                    if m % 12 == 0:  # Record yearly values for plot
                        values.append(current)
                years_list = list(range(1, years + 1))
            
            ax.plot(years_list, values, marker='o', linewidth=2, color='#2196F3')
            ax.set_title(reshape_arabic(trans['invest_title'], lang), fontsize=16, fontweight='bold')
            ax.set_xlabel(reshape_arabic(trans['invest_xlabel'], lang), fontsize=12)
            ax.set_ylabel(reshape_arabic(trans['invest_ylabel'], lang), fontsize=12)
            ax.grid(True)
            
            for i, val in enumerate(values):
                ax.text(years_list[i], val, f'{val:.2f}', ha='center', va='bottom', fontsize=10)

        elif calc_type == 'budget':
            income = inputs['income']
            expenses = inputs['expenses']
            remaining = income - expenses
            
            labels = [reshape_arabic(label, lang) for label in trans['budget_labels']]
            sizes = [expenses, max(0, remaining)]  # Avoid negative
            colors = ['#F44336', '#4CAF50']
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                   shadow=True, startangle=90, textprops={'fontsize': 12})
            ax.set_title(reshape_arabic(trans['budget_title'].format(income=income), lang), fontsize=16, fontweight='bold')
            ax.axis('equal')

        else:
            return jsonify({'error': 'Invalid calculator type'}), 400

        # Convert to base64 PNG
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({'image': f'data:image/png;base64,{img_base64}'})
    except Exception as e:
        print(f"Error generating graph for {calc_type}: {str(e)}")
        return jsonify({'error': 'Graph generation failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)