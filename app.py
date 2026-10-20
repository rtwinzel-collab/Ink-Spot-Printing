import streamlit as st
import random
from datetime import datetime

# --- EMAIL SIMULATOR MODE ---
def send_simulated_email(to_email, student_name, order_id, status, payment_status):
    """Simulates a live email notification instantly for presentation purposes."""
    return True, f"Simulated email successfully sent to {to_email} inbox!"

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Ink Spot Printing Studio", page_icon="🖨️", layout="centered")

# --- MOCK DATABASE & ARCHIVE STORAGE ---
if "print_queue" not in st.session_state:
    st.session_state.print_queue = [
        {"id": "PRT-1001", "student": "Maria Santos", "filename": "Thesis_Chapter1.pdf", "file_obj": None, "service": "Print", "details": "1 Copy (Colored) - A4", "payment": "Unpaid (Pay at Counter)", "email": "maria@gmail.com", "status": "In Queue - Position #1", "total": 10.00},
        {"id": "PRT-1002", "student": "Hanna Ramirez", "filename": "Activity_Sheet.docx", "file_obj": None, "service": "Xerox", "details": "2 Copies - Short", "payment": "Unpaid (Pay at Counter)", "email": "hanna@gmail.com", "status": "In Queue - Position #2", "total": 10.00},
        {"id": "PRT-1003", "student": "Sofia Fernandez", "filename": "ID_Picture.png", "file_obj": None, "service": "Develop", "details": "1 Copy (Colored) - Standard", "payment": "Paid in Advance", "email": "sofia@gmail.com", "status": "In Queue - Position #3", "total": 30.00},
        {"id": "PRT-1004", "student": "Lea Mae", "filename": "Certificate.pdf", "file_obj": None, "service": "Laminate", "details": "1 Copy - Long", "payment": "Unpaid (Pay at Counter)", "email": "leamae@gmail.com", "status": "In Queue - Position #4", "total": 35.00}
    ]

if "archived_orders" not in st.session_state:
    st.session_state.archived_orders = []

if "selected_receipt" not in st.session_state:
    st.session_state.selected_receipt = None

st.title("🖨️ Ink Spot Printing Studio")
st.markdown("---")

# Sidebar Navigation
user_role = st.sidebar.selectbox("Select View:", ["Student Portal", "Shop Owner POS Dashboard", "Archived Orders History"])

# ==========================================
# 1. STUDENT PORTAL
# ==========================================
if user_role == "Student Portal":
    st.subheader("📄 Create Service Request")
    
    with st.form("print_form"):
        student_name = st.text_input("Student Name")
        student_email = st.text_input("Email Address")
        
        uploaded_file = st.file_uploader("Upload File (PDF, Word, PNG, JPG)", type=["pdf", "docx", "png", "jpg", "jpeg"])
        
        st.markdown("---")
        st.markdown("### ⚙️ Service Options")
        
        service_offered = st.selectbox("Select Service", ["Print", "Xerox", "Laminate", "Develop"])
        color_option = st.selectbox("Color Option", ["Black & White", "Colored"])
        paper_size = st.selectbox("Paper Size", ["Short", "Long", "A4"])
        num_copies = st.number_input("Number of Copies:", min_value=1, value=1)
        
        submitted = st.form_submit_button("Submit Request")
        
        if submitted and student_name and student_email and uploaded_file:
            if service_offered == "Print":
                rate = 5 if color_option == "Black & White" else 10
            elif service_offered == "Xerox":
                rate = 5
            elif service_offered == "Laminate":
                rate = 35
            else: # Develop
                rate = 30
                
            total_cost = rate * num_copies
            order_id = f"PRT-{random.randint(1005, 9999)}"
            status_text = f"In Queue - Position #{len(st.session_state.print_queue) + 1}"
            
            details_summary = f"{num_copies} Copy/ies ({color_option}) - {paper_size}"

            new_job = {
                "id": order_id,
                "student": student_name,
                "filename": uploaded_file.name,
                "file_obj": uploaded_file,
                "service": service_offered,
                "details": details_summary,
                "payment": "Unpaid (Pay at Counter)",
                "email": student_email,
                "status": status_text,
                "total": total_cost
            }
            st.session_state.print_queue.append(new_job)
            
            st.success(f"Order successfully submitted! Your Order ID is *{order_id}*.")
            st.info(f"Total Amount Due: *₱{total_cost:.2f}* | Track status below using your Order ID.")

    st.markdown("---")
    st.markdown("### 🔍 Track Your Personal Order Status & Document")
    search_query = st.text_input("Enter Order ID (e.g. PRT-1001) or Email:")
    
    if search_query:
        found_orders = [
            job for job in st.session_state.print_queue 
            if search_query.strip().lower() in job['id'].lower() or search_query.strip().lower() in job['email'].lower()
        ]
        
        if found_orders:
            for job in found_orders:
                st.success(f"*Live Status for {job['student']} ({job['id']})*")
                st.info(f"🔔 *Current Status Notification:* {job['status']}")
                st.write(f"*Service:* {job['service']} ({job['details']})")
                st.write(f"*Payment Status:* {job['payment']}")
                st.write(f"*Total Amount:* ₱{job['total']:.2f}")
                
                st.markdown("---")
                st.write(f"📁 *Your Uploaded Document:* {job['filename']}")
                if "file_obj" in job and job['file_obj'] is not None:
                    file_type = job['filename'].split('.')[-1].lower()
                    if file_type in ['png', 'jpg', 'jpeg']:
                        st.image(job['file_obj'], caption=job['filename'], width=300)
                    else:
                        st.write(f"*(Document file {job['filename']} is attached successfully.)*")
                
                if st.button("❌ Cancel My Order", key=f"cancel_personal_{job['id']}"):
                    st.session_state.print_queue = [j for j in st.session_state.print_queue if j['id'] != job['id']]
                    st.warning(f"Order {job['id']} has been cancelled.")
                    st.rerun()
        else:
            st.error("No active order found with that Order ID or Email.")

# ==========================================
# 2. SHOP OWNER POS DASHBOARD
# ==========================================
elif user_role == "Shop Owner POS Dashboard":
    st.subheader("💻 Shop Owner POS Dashboard")

    if st.session_state.selected_receipt:
        receipt_data = st.session_state.selected_receipt
        st.markdown("---")
        st.subheader("🧾 OFFICIAL RECEIPT PAGE")
        st.info("Present or save this digital page as proof of transaction.")
        
        st.markdown(f"""
        *INK SPOT PRINTING STUDIO*  
        Campus Branch, Main Avenue  
        
        ---
        *Date & Time:* {receipt_data['timestamp']}  
        *Order ID:* {receipt_data['id']}  
        *Customer:* {receipt_data['student']}  
        *File:* {receipt_data['filename']}  
        *Email:* {receipt_data['email']}  
        *Service:* {receipt_data['service']}  
        *Details:* {receipt_data['details']}  
        *Payment Status:* {receipt_data['payment']}  
        *Total Amount:* ₱{receipt_data['total']:.2f}  
        *Status:* PAID / COMPLETED & ARCHIVED  
        ---
        Thank you for choosing Ink Spot Printing Studio!
        """)
        
        if st.button("Close Receipt View"):
            st.session_state.selected_receipt = None
            st.rerun()
        st.markdown("---")

    if not st.session_state.print_queue:
        st.warning("No current orders in the queue.")
    else:
        for index, job in enumerate(st.session_state.print_queue):
            with st.expander(f"Order: {job['id']} - {job['student']} ({job['payment']}) | Status: {job['status']}"):
                st.write(f"*Customer Email:* {job['email']}")
                st.write(f"*Service:* {job['service']} ({job['details']})")
                st.write(f"*Total Amount:* ₱{job['total']:.2f}")
                
                st.markdown("---")
                st.write(f"📄 *Uploaded Document/File by Student:* {job['filename']}")
                if "file_obj" in job and job['file_obj'] is not None:
                    file_type = job['filename'].split('.')[-1].lower()
                    if file_type in ['png', 'jpg', 'jpeg']:
                        st.image(job['file_obj'], caption=f"Owner View: {job['filename']}", width=350)
                    else:
                        st.info(f"💡 Shop Owner Note: Document {job['filename']} is ready to be printed.")
                else:
                    st.write("(Default Demo File / Sample Record)")
                st.markdown("---")
                
                current_pay_idx = 0 if job['payment'] == "Unpaid (Pay at Counter)" else 1
                updated_payment = st.selectbox(
                    "Update Payment Status (Shop Owner Only):", 
                    ["Unpaid (Pay at Counter)", "Paid in Advance"], 
                    index=current_pay_idx, 
                    key=f"pay_update_{index}"
                )
                
                if updated_payment != job['payment']:
                    st.session_state.print_queue[index]['payment'] = updated_payment
                    st.success("Payment status updated successfully!")
                    st.rerun()

                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("Start Printing", key=f"print_{index}"):
                        st.session_state.print_queue[index]['status'] = "Processing... (Printing in progress)"
                        st.success(f"Status updated to Processing for {job['student']}!")
                        st.rerun()
                        
                with col2:
                    if st.button("Ready & Email", key=f"ready_{index}"):
                        st.session_state.print_queue[index]['status'] = "Ready for Pickup"
                        
                        # Simulated email dispatch
                        success, msg = send_simulated_email(
                            to_email=job['email'],
                            student_name=job['student'],
                            order_id=job['id'],
                            status="Ready for Pickup",
                            payment_status=job['payment']
                        )
                        
                        st.success(f"📩 SUCCESS: Notification email successfully dispatched to *{job['email']}* inbox!")
                        st.rerun()

                with col3:
                    if st.button("Done & Archive", key=f"done_{index}"):
                        completed_job = st.session_state.print_queue.pop(index)
                        completed_job['timestamp'] = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                        st.session_state.archived_orders.append(completed_job)
                        st.session_state.selected_receipt = completed_job
                        st.balloons()
                        st.rerun()

                with col4:
                    if st.button("🗑️ Delete", key=f"del_pos_{index}"):
                        deleted_job = st.session_state.print_queue.pop(index)
                        st.warning(f"Deleted order {deleted_job['id']}.")
                        st.rerun()

# ==========================================
# 3. ARCHIVED ORDERS HISTORY
# ==========================================
else:
    st.subheader("📁 Archived Orders & Transaction History")
    st.write("Use this page to verify completed transactions with exact timestamps for customer inquiries or reclamations.")

    if not st.session_state.archived_orders:
        st.info("No archived transactions yet.")
    else:
        for index, item in enumerate(reversed(st.session_state.archived_orders)):
            original_index = len(st.session_state.archived_orders) - 1 - index
            with st.expander(f"Archived Order: {item['id']} - {item['student']} | Payment: {item['payment']}"):
                st.write(f"*Date & Time Completed:* {item['timestamp']}")
                st.write(f"*Customer Name:* {item['student']}")
                st.write(f"*File Name:* {item['filename']}")
                st.write(f"*Email Address:* {item['email']}")
                st.write(f"*Service Rendered:* {item['service']}")
                st.write(f"*Details:* {item['details']}")
                st.write(f"*Payment Status:* {item['payment']}")
                st.write(f"*Total Amount:* ₱{item['total']:.2f}")
                st.write("*Status:* Completed & Stored in Archive")
                
                if st.button("🗑️ Delete Archive Record", key=f"del_archive_{original_index}"):
                    st.session_state.archived_orders.pop(original_index)
                    st.success("Record deleted from archive history.")
                    st.rerun()