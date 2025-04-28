import streamlit as st
import joblib

def run_app():
    # Load the trained model and scaler
    model = joblib.load('model.joblib')  # Load the trained model
    scaler = joblib.load('scaler.joblib')  # Load the fitted scaler

    # Define label translations for multilingual support
    labels = {
        'en': {
            "app_title": "AI Model For Bank Customer Churn Prediction",
            "title": "Customer Data",
            'Age': 'Age',
            'Balance': 'Balance',
            'Credit Score': 'Credit Score',
            'Gender': 'Gender',
            'Male': 'Male',
            'Female': 'Female',
            'Active Member': 'Active Member',
            'Active': 'Active',
            'Not Active': 'Not Active',
            'Geography': 'Geography',
            'Geography Options': ['France', 'Germany', 'Spain'],
            'Number of Products': 'Number of Products',
            'Credit Card Ownership': 'Credit Card Ownership',
            'Submit': 'Submit',
            'Prediction': 'Prediction',
            'Churn Prediction': 'Customer Churn Prediction'
        },
        'ar': {
            "app_title": "نموذج ذكاء اصطناعي لتوقع مغادرة عملاء البنك",
            "title": "بيانات العميل",
            'Age': 'العمر',
            'Balance': 'الرصيد',
            'Credit Score': 'درجة الائتمان',
            'Gender': 'الجنس',
            'Male': 'ذكر',
            'Female': 'أنثى',
            'Active Member': 'عضو نشط',
            'Active': 'نشط',
            'Not Active': 'غير نشط',
            'Geography': 'المنطقة',
            'Geography Options': ['فرنسا', 'ألمانيا', 'إسبانيا'],
            'Number of Products': 'عدد المنتجات',
            'Credit Card Ownership': 'امتلاك بطاقة ائتمان',
            'Submit': 'إرسال',
            'Prediction': 'التنبؤ',
            'Churn Prediction': 'تنبؤ مغادرة العميل'
        }
    }

    # Custom CSS for UI styling
    custom_css = """
    <style>
        .title-box {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: white;
            background-color: gray;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        body {
            overflow: hidden;
        }
        .main {
            max-height: 100vh;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Language selection dropdown
    language = st.selectbox('Select Language / اختر اللغة', ['English', 'عربي'])
    lang_code = 'ar' if language == 'عربي' else 'en'

    # Show title based on selected language
    st.markdown(f'<div class="title-box">{labels[lang_code]["app_title"]}</div>', unsafe_allow_html=True)

    # If Arabic, apply RTL styling
    if lang_code == 'ar':
        rtl_css = """<style>body { direction: rtl; text-align: right; }</style>"""
        st.markdown(rtl_css, unsafe_allow_html=True)

    # Show welcome message
    if lang_code == 'ar':
        welcome_message = "مرحبًا بك في تطبيق التنبؤ بمغادرة عملاء البنك. من فضلك أدخل بيانات العميل للحصول على التوقع."
    else:
        welcome_message = "Welcome to the Bank Customer Churn Prediction App. Please enter customer data to get a prediction."
    st.success(welcome_message)

    # Section title
    st.markdown(f"### *{labels[lang_code]['title']}*")

    # Create a 2-row, 3-column layout for form inputs
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    # First row of inputs
    with col1:
        credit_score = st.number_input(labels[lang_code]['Credit Score'], min_value=300, max_value=850)
    with col2:
        balance = st.number_input(labels[lang_code]['Balance'], min_value=0.0)
    with col3:
        gender = st.selectbox(labels[lang_code]['Gender'], [labels[lang_code]['Male'], labels[lang_code]['Female']])

    # Second row of inputs
    with col4:
        active_member_display = st.selectbox(labels[lang_code]['Active Member'], [labels[lang_code]['Active'], labels[lang_code]['Not Active']])
        active_member = 1 if active_member_display == labels[lang_code]['Active'] else 0
    with col5:
        geography = st.selectbox(labels[lang_code]['Geography'], labels[lang_code]['Geography Options'])
    with col6:
        products = st.number_input(labels[lang_code]['Number of Products'], min_value=1, max_value=4)

    # Additional input for Age
    age = st.number_input(labels[lang_code]['Age'], min_value=18, max_value=100)

    # Submit button to make prediction
    if st.button(labels[lang_code]['Submit']):
        # Calculate ageskewed based on geography
        if geography == labels[lang_code]['Geography Options'][0]:  # France
            ageskewed = age / 1.5
        elif geography == labels[lang_code]['Geography Options'][1]:  # Germany
            ageskewed = age / 1.2
        else:  # Spain
            ageskewed = age / 1.1

        # Prepare input data as a dictionary
        data = {
            'creditscore': credit_score,
            'balance': balance,
            'numofproducts': products,
            'genderlabel': 1 if gender == labels[lang_code]['Male'] else 0,
            'ageskewed': ageskewed,
            'isactivemember': active_member,
            'geographyfrance': 1 if geography == labels[lang_code]['Geography Options'][0] else 0,
            'geographygermany': 1 if geography == labels[lang_code]['Geography Options'][1] else 0,
            'geographyspain': 1 if geography == labels[lang_code]['Geography Options'][2] else 0
        }

        # Scale input data using the loaded scaler
        scaled_data = scaler.transform([list(data.values())])

        # Make prediction using the trained model
        prediction = model.predict(scaled_data)[0]

        # Display result inside a gray styled HTML box
        st.subheader(labels[lang_code]['Prediction'])

        if prediction == 1:
            message = "من المحتمل أن يغادر العميل البنك" if lang_code == 'ar' else "The Customer May Leave The Bank."
        else:
            message = "العميل لم يغادر البنك" if lang_code == 'ar' else "The Customer Still In The Bank."

        # Gray color box
        html_code = f"""
        <div style='background-color: #6c757d; padding: 20px; border-radius: 10px; color: white; text-align: center; font-size: 20px; font-weight: bold;'>
            {labels[lang_code]['Churn Prediction']}<br><br>{message}
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    run_app()
