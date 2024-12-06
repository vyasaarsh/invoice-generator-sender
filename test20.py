import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import pywhatkit
import pyautogui
import time
import os

# Function to generate invoice PDF
from datetime import datetime

# Function to generate invoice PDF
def create_invoice_pdf(company_name, company_slogan, logo_path, name, phone, file_path, descriptions, quantities, prices, alteration, remarks):
    totals = [qty * price for qty, price in zip(quantities, prices)]
    total_amount = sum(totals)
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    # Company Branding (Logo and Company Name)
    styles = getSampleStyleSheet()
    
    # Logo and Company Name
    logo = Image(logo_path, width=55, height=55)
    company_title = Paragraph(
        f"<font color='red'><b>{company_name}</b></font>",
        styles["Title"]
    )
    company_address = Paragraph(
    "PLOT NO. 28,29,31, GHANSHYAM IND. ESTATE, AT VASNA TAL - SANAND, VILLAGE VASANA IYAVAM DIST., AHMEDABAD - 382110<br/>Phone Number: +919898316996",
    styles["BodyText"]
    )
    #company_title = Paragraph(f"<b>{company_name}</b>", styles["Heading1"])
    #company_slogan_text = Paragraph(company_slogan, styles["BodyText"])
    
    # Combine logo, company name, and address in the same row
    company_header = Table(
        [[logo, company_title, company_address]], 
        colWidths=[120, 134, 296]
    )
    company_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # Vertical alignment for logo
        ('VALIGN', (1, 0), (-1, 0), 'MIDDLE'),  # Vertical alignment for text
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Center-align the logo in its cell
        ('ALIGN', (1, 0), (-1, 0), 'LEFT'),  # Left-align text
        ('LEFTPADDING', (1, 0), (-1, -1), 5),  # Adjust padding
        ('RIGHTPADDING', (1, 0), (-1, -1), 5),  
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Adjust vertical space
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10), 
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)
    ]))

    elements.append(company_header)
    #elements.append(Spacer(1, 50))  # Width=1, Height=20 points

    # Date row
    current_date = datetime.now().strftime("%B %d, %Y")
    date_row = Table([[f"INVOICE", f"Date: {current_date}"]], colWidths=[350, 200])
    #date_row = Table([[f"Date: {current_date}"]], colWidths=[550])
    date_row.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Left-align INVOICE
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Right-align Date
        ('TEXTCOLOR', (0, 0), (0, 0), colors.black),  # Navy blue for INVOICE
        ('TEXTCOLOR', (1, 0), (1, 0), colors.black),  # Black for date
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),  # Bold for INVOICE
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),  # Bold for date
        ('FONTSIZE', (0, 0), (0, 0), 16),  # Increase font size for INVOICE
        ('FONTSIZE', (1, 0), (1, 0), 16),  # Increase font size for date
        ('PADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # Increased bottom padding
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)
    ]))

    elements.append(date_row)
    #elements.append(Paragraph(" ", styles["BodyText"]))
    elements.append(Spacer(1, 20))  # Width=1, Height=20 points

    # Customer Information
    customer_info = Table([[f"NAME: {name}", f"PHONE: {phone}"]], colWidths=[350, 200])
    customer_info.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(customer_info)
    #elements.append(Paragraph(" ", styles["BodyText"]))
    elements.append(Spacer(1, 20))  # Width=1, Height=20 points

    # Alteration and Remarks
    alteration_remarks_data = [
        [f"ALTERATION: {alteration}"],
        [f"REMARKS: {remarks}"],
        [f"PAYMENT: {st.session_state.payment_method}"]
    ]
    alteration_remarks_table = Table(alteration_remarks_data, colWidths=[550])
    alteration_remarks_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)
    ]))

    elements.append(alteration_remarks_table)
    #elements.append(Paragraph(" ", styles["BodyText"]))
    elements.append(Spacer(1, 20))  # Width=1, Height=20 points

    # Table data setup
    data = [["DESCRIPTION", "QUANTITY", "PRICE", "TOTAL"]]  # Table header
    for desc, qty, price, total in zip(descriptions, quantities, prices, totals):
        data.append([desc, qty, f"Rs. {price:.2f}", f"Rs. {total:.2f}"])
    

    # Total row
    #data.append(["Total", f"Rs. {total_amount:.2f}"])

    # Table styling
    table = Table(data, colWidths=[250, 100, 100, 100])
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey) 
    ]))

    elements.append(table)

     # Create a continuation table with 2 columns for total
    total_data = [["TOTAL", f"Rs. {total_amount:.2f}"]]
    total_table = Table(total_data, colWidths=[450, 100])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),  # Right-align TOTAL
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),   # Left-align amount
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
        ('BOTTOMPADDING', (0, 0), (1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(total_table)

    #footer_text = "Thank you for shopping with us! Please reach out if you have any questions."
    #footer_table = Table([[footer_text]], colWidths=[550])
    #footer_table.setStyle(TableStyle([
     #   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      #  ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
       # ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
      #  ('FONTSIZE', (0, 0), (-1, -1), 10),
       # ('TOPPADDING', (0, 0), (-1, -1), 20)
   # ]))

    #elements.append(Spacer(1, 349))  # Space before footer
    #elements.append(footer_table)

    # Payment and Terms
    #payment_info = Paragraph("Payment Due: 14 days | Accepted Methods: Visa, Mastercard, PayPal", styles["BodyText"])
    #terms_conditions = Paragraph("Terms and Conditions apply. See website for details.", styles["BodyText"])
    #elements.append(Paragraph(" ", styles["BodyText"]))
    #elements.append(payment_info)
    #elements.append(terms_conditions)
   
    doc.build(elements)

# Function to send the PDF via WhatsApp
def send_pdf_via_whatsapp(phone_number, file_path):
    if not os.path.isfile(file_path):
        st.error("Error: PDF file does not exist.")
        return
    
    try:
        pywhatkit.sendwhatmsg_instantly(phone_number, "Thankyou for shopping with BINDI INDIA! Here is your invoice.")
        time.sleep(10)  # Adjust as needed for WhatsApp to load
        pyautogui.click(x=577, y=863)
        time.sleep(3)
        pyautogui.click(x=642, y=599)
        time.sleep(3)
        absolute_file_path = os.path.abspath(file_path)
        pyautogui.write(absolute_file_path, interval=0.4)
        pyautogui.press('enter')
        #pyautogui.write(file_path)
        #pyautogui.press('return')
        time.sleep(5)
        pyautogui.press('enter')
        time.sleep(5)
        pyautogui.press('enter')
        st.success("PDF sent via WhatsApp.")
    except Exception as e:
        st.error(f"Error sending PDF via WhatsApp: {e}")

# Streamlit UI
def main():
    st.title("Invoice Generator and Sender")
    st.subheader("Fill out the form to create and send an invoice via WhatsApp")

    # Initialize session state for form fields
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'phone' not in st.session_state:
        st.session_state.phone = ''
    if 'num_items' not in st.session_state:
        st.session_state.num_items = 1
    if 'alteration' not in st.session_state:
        st.session_state.alteration = 'No'
    if 'remarks' not in st.session_state:
        st.session_state.remarks = ''

    # Input fields
    st.session_state.name = st.text_input("Customer Name", value=st.session_state.name, key='name_input')
    st.session_state.phone = st.text_input(
        "Phone Number (with country code, e.g., +123456789)",
        value=st.session_state.phone,
        key='phone_input'
    )

    # Alteration and Remarks Section
    st.write("### Alteration Details")
    st.session_state.alteration = st.radio(
        "Alteration Required?",
        options=["Yes", "No"],
        index=0 if st.session_state.alteration == 'Yes' else 1,
        key='alteration_radio'
    )
    st.session_state.remarks = st.text_area(
        "Remarks (if any)",
        value=st.session_state.remarks,
        key='remarks_input'
    )

    # Payment Method Section
    st.write("### Payment Method")
    st.session_state.payment_method = st.radio(
        "Select Payment Method:",
        options=["Online", "Cash"],
        index=0,  # Default to "Online"
        key='payment_method_radio'
    )

    st.write("### Add Invoice Items")
    st.session_state.num_items = st.number_input(
        "Number of Items",
        min_value=1,
        value=st.session_state.num_items,
        step=1,
        key='num_items_input'
    )

    # Dynamic item inputs
    descriptions = []
    quantities = []
    prices = []
    for i in range(st.session_state.num_items):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            desc = st.text_input(
                f"Description for Item {i + 1}",
                key=f"desc_{i}",
                value=st.session_state.get(f'desc_{i}', '')
            )
        
        with col2:
            qty = st.number_input(
                f"Quantity",
                min_value=1,
                key=f"qty_{i}",
                value=st.session_state.get(f'qty_{i}', 1)
            )
        
        with col3:
            price = st.number_input(
                f"Price per Unit",
                min_value=0.0,
                key=f"price_{i}",
                value=st.session_state.get(f'price_{i}', 0.0)
            )
        
        descriptions.append(desc)
        quantities.append(qty)
        prices.append(price)

    # Calculate total amount dynamically
    totals = [qty * price for qty, price in zip(quantities, prices)]
    total_amount = sum(totals)

    # Display Total's Box at the top
    st.write("### Invoice Summary")
    st.info(f"**Total Amount: Rs.{total_amount:.2f}**")

    # Display the items entered so far
    if descriptions:
        st.write("### Items Entered")
        for idx, (desc, qty, price, total) in enumerate(zip(descriptions, quantities, prices, totals), 1):
            st.write(f"{idx}. **{desc}** - Qty: {qty}, Price: Rs.{price:.2f}, Total: Rs.{total:.2f}")

    # Buttons column
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        generate_button = st.button("Generate and Send Invoice", use_container_width=True)

    with col2:
        save_button = st.button("Generate and Save Invoice", use_container_width=True)

    with col3:
        clear_button = st.button("Clear Form", use_container_width=True)

    # Handle form submission
    if generate_button:
        if st.session_state.name and st.session_state.phone and descriptions and quantities and prices:
            pdf_file_path = os.path.join("/Users/aarsh/Desktop/Invoices", f"{st.session_state.name}_invoice.pdf")
            create_invoice_pdf(
                "", "",
                "https://github.com/vyasaarsh/invoice-generator-sender/blob/main/Logo/logo.png",
                st.session_state.name,
                st.session_state.phone,
                pdf_file_path,
                descriptions,
                quantities,
                prices,
                alteration=st.session_state.alteration,
                remarks=st.session_state.remarks
            )
            st.success(f"Invoice created: {pdf_file_path}")
            send_pdf_via_whatsapp(st.session_state.phone, pdf_file_path)
        else:
            st.error("Please fill out all fields.")

    # Handle form submission for generating and saving the invoice only
    if save_button:
        if st.session_state.name and descriptions and quantities and prices:
            pdf_file_path = os.path.join("/Users/aarsh/Desktop/Invoices", f"{st.session_state.name}_invoice.pdf")
            create_invoice_pdf(
                "", "",
                "https://github.com/vyasaarsh/invoice-generator-sender/blob/main/Logo/logo.png",
                st.session_state.name,
                st.session_state.phone,
                pdf_file_path,
                descriptions,
                quantities,
                prices,
                alteration=st.session_state.alteration,
                remarks=st.session_state.remarks
            )
            st.success(f"Invoice saved as: {pdf_file_path}")
        else:
            st.error("Please fill out all fields.")

    # Handle form clearing
    if clear_button:
        # Reset all session state variables
        st.session_state.name = ''
        st.session_state.phone = ''
        st.session_state.alteration = 'No'
        st.session_state.remarks = ''
        st.session_state.num_items = 1

        # Clear dynamic item inputs
        for i in range(10):  # Clear up to 10 potential item fields
            if f'desc_{i}' in st.session_state:
                del st.session_state[f'desc_{i}']
            if f'qty_{i}' in st.session_state:
                del st.session_state[f'qty_{i}']
            if f'price_{i}' in st.session_state:
                del st.session_state[f'price_{i}']

        # Rerun the app to reset the form
        st.rerun()

# Run the main function
if __name__ == "__main__":
    main()