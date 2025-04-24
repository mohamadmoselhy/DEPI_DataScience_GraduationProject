import streamlit as st

def run_app():
    # Label translations
    labels = {
        'en': {
            "title": "Customer Data",
            'Age': 'Age',
            'Balance': 'Balance',
            'Credit Score': 'Credit Score',
            'Gender': 'Gender',
            'Active Member': 'Active Member',
            'Geography': 'Geography',
            'Tenure (Years)': 'Tenure (Years)',
            'Number of Products': 'Number of Products',
            'Credit Card Ownership': 'Credit Card Ownership',
            'Submit': 'Submit',
            'Collected Data': 'Collected Data',
            'Form submitted successfully!': 'Form submitted successfully!'
        },
        'ar': {
            "title": " بيانات العميل",
            'Age': 'العمر',
            'Balance': 'الرصيد',
            'Credit Score': 'درجة الائتمان',
            'Gender': 'الجنس',
            'Active Member': 'عضو نشط',
            'Geography': 'المنطقة',
            'Tenure (Years)': 'مدة الاشتراك (بالسنوات)',
            'Number of Products': 'عدد المنتجات',
            'Credit Card Ownership': 'امتلاك بطاقة ائتمان',
            'Submit': 'إرسال',
            'Collected Data': 'البيانات المجمعة',
            'Form submitted successfully!': 'تم إرسال النموذج بنجاح!'
        }
    }

    # Language selection
    language = st.selectbox('Select Language / اختر اللغة', ['English', 'Arabic'])
    lang_code = 'ar' if language == 'Arabic' else 'en'

    # Inject basic RTL support for Arabic
    if lang_code == 'ar':
        rtl_css = """<style>body { direction: rtl; text-align: right; }</style>"""
        st.markdown(rtl_css, unsafe_allow_html=True)

    # Title
    st.markdown(f"### **{labels[lang_code]['title']}**")

    # Form layout in 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input(labels[lang_code]['Age'], min_value=18, max_value=120)
        balance = st.number_input(labels[lang_code]['Balance'], min_value=0)
        credit_score = st.number_input(labels[lang_code]['Credit Score'], min_value=300, max_value=850)

    with col2:
        gender = st.selectbox(labels[lang_code]['Gender'], ['Male', 'Female'])
        active_member = st.selectbox(labels[lang_code]['Active Member'], ['Yes', 'No'])
        geography = st.selectbox(labels[lang_code]['Geography'], ['Frence', 'Germany', 'Spain'])

    with col3:
        tenure = st.number_input(labels[lang_code]['Tenure (Years)'], min_value=0, max_value=100)
        products = st.number_input(labels[lang_code]['Number of Products'], min_value=1)
        credit_card = st.selectbox(labels[lang_code]['Credit Card Ownership'], ['Yes', 'No'])

    # Submit button
    if st.button(labels[lang_code]['Submit']):
        data = {
            labels[lang_code]['Age']: age,
            labels[lang_code]['Balance']: balance,
            labels[lang_code]['Credit Score']: credit_score,
            labels[lang_code]['Gender']: gender,
            labels[lang_code]['Active Member']: active_member,
            labels[lang_code]['Geography']: geography,
            labels[lang_code]['Tenure (Years)']: tenure,
            labels[lang_code]['Number of Products']: products,
            labels[lang_code]['Credit Card Ownership']: credit_card
        }

        st.subheader(labels[lang_code]['Collected Data'])
        st.json(data)
        st.success(labels[lang_code]['Form submitted successfully!'])

# Run the app
if __name__ == "__main__":
    run_app()
