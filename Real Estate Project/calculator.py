import os
import matplotlib.pyplot as plt
import seaborn as sns
import jinja2
import pdfkit
import xlsxwriter
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Function to get valid input
def get_valid_input(prompt, input_type=float):
    while True:
        try:
            return input_type(input(prompt).replace(',', ''))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Function to print user information
def print_user_info(name, address, state, zip_code, company_name, city):
    print("Name:", name)
    print("Address:", address)
    print("State: ", state)
    print("City: ", city)
    print("Zip Code: ", zip_code)
    print("Company Name: ", company_name)


# Function to attach file to email
def attach_file_to_email(message, filename):
    # Open the file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(filename)}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)


# Function to calculate costs
def calculate_financing_costs(loan_amount, loan_interest, loan_months):
    return ((loan_interest * loan_amount) / 12) * loan_months


# Function to calculate holding costs
def calculate_total_holding(holding_cost, holding_months):
    return holding_cost * holding_months


# Function to calculate closing costs
def calculate_closing_costs(closing_cost_percentage, purchase_price):
    return closing_cost_percentage * purchase_price


# Function to calculate selling costs
def calculate_selling_costs(selling_costs, selling_price):
    return selling_costs * selling_price


# Function to calculate total investment
def calculate_total_investment(purchase_price, renovation_cost, total_holding, total_selling_costs, total_closing, financing_costs):
    return purchase_price + renovation_cost + total_holding + total_selling_costs + total_closing + financing_costs


# Function to calculate total profit
def calculate_total_profit(selling_price, total_investment, earnest_money, contingency):
    return selling_price - total_investment + earnest_money - contingency


# Function to calculate cash invested
def calculate_cash_invested(upfront_project_costs, loan_amount):
    return abs(upfront_project_costs - loan_amount)


# Function to calculate cash on cash
def calculate_cash_on_cash_return(total_profit, cash_invested):
    return abs(total_profit / cash_invested)


# Function to calculate upfront project costs
def upfront_project_costs(purchase_price, renovation_cost, earnest_money, total_holding, total_closing, financing_costs):
    return purchase_price + renovation_cost + earnest_money + total_holding + total_closing + financing_costs


# Function to print profit information
def print_profit_info(total_profit, desired_profit, profit_information):
    if total_profit < desired_profit:
        profit_difference = abs(total_profit - desired_profit)
        profit_information = (f"Your desired profit was ${desired_profit:,.2f}.\n"
              f"You were not able to reach your desired profit.\n"
              f"You are off by ${profit_difference:,.2f} in terms of projected profit. \n")
    else:
        profit_surplus = abs(total_profit - desired_profit)
        profit_information = (f"Your desired profit was ${desired_profit:,.2f}.\n"
              f" You are above your desired profit by ${profit_surplus:,.2f} in terms of projected profit.\n"
              " You were able to reach or exceed your desired profit! \n")

    return profit_information


# Function to plot investment vs profit
def plot_investment_vs_profit(purchase_price, renovation_cost, holding_cost, closing_cost, total_investment, total_profit):
    categories = ['Purchase Price', 'Renovation Cost', 'Holding Cost', 'Closing Cost', 'Total Investment', 'Total Profit']
    values = [purchase_price, renovation_cost, holding_cost, closing_cost, total_investment, total_profit]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=categories, y=values, palette='muted', hue=categories, dodge=False, legend=False)
    plt.title('Investment Breakdown and Profit')
    plt.xlabel('Category')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("investment_vs_profit.png")
    plt.close()


# Function to plot cost breakdown
def plot_cost_breakdown(purchase_price, renovation_cost, holding_cost, closing_cost, total_selling_costs, financing_costs):
    labels = ['Purchase Price', 'Renovation Cost', 'Holding Cost', 'Closing Cost', 'Selling Costs', 'Financing Costs']
    sizes = [purchase_price, renovation_cost, holding_cost, closing_cost, total_selling_costs, financing_costs]
    colors = sns.color_palette('muted', len(labels))

    plt.figure(figsize=(9, 9))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Cost Breakdown', y=1.08, x=0.55)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("cost_breakdown.png")
    plt.close()


# Function to calculate profit
def profit_calculations():
    print("Real Estate Flipping Calculator Tool\nPut 0 for n/a")
    print("----------------------------------------------------------------------------------------------------------------- \n")

    name = input("Enter your name: ")
    address = input("Enter flipping address: ")
    state = input("Enter state: ")
    city = input("Enter city: ")
    zip_code = input("Enter zip code: ")
    company_name = input("Enter your company name: ")
    print("----------------------------------------------------------------------------------------------------------------- \n")

    print("User information: \n")
    print_user_info(name, address, state, zip_code, company_name,city)

    print("----------------------------------------------------------------------------------------------------------------- \n")

    purchase_price = get_valid_input("Enter purchase price: $", int)
    renovation_cost = get_valid_input("Enter renovation cost: $")
    earnest_money = get_valid_input("Enter earnest money: $")
    holding_cost = get_valid_input("Enter holding cost per month: $")
    holding_months = get_valid_input("Enter total months for holding costs: ", int)
    closing_cost_percentage = get_valid_input("Enter closing cost percentage: ") / 100
    selling_price = get_valid_input("Enter resale value of the property: $")
    selling_costs = get_valid_input("Enter selling cost percentage: ") / 100
    loan_amount = get_valid_input("Enter loan amount: $", int)
    loan_interest = get_valid_input("Enter loan interest rate: ") / 100
    loan_months = get_valid_input("Enter loan months: ", int)
    contingency_one_time_costs = get_valid_input("Enter contingency/one time costs costs: ")
    desired_profit = get_valid_input("Enter your desired profit: $")

    # Calculations
    financing_costs = calculate_financing_costs(loan_amount, loan_interest, loan_months)
    total_holding = calculate_total_holding(holding_cost, holding_months)
    total_closing = calculate_closing_costs(closing_cost_percentage, purchase_price)
    total_selling_costs = calculate_selling_costs(selling_costs, selling_price)
    total_investment = calculate_total_investment(purchase_price, renovation_cost, total_holding, total_selling_costs, total_closing, financing_costs)
    total_profit = calculate_total_profit(selling_price, total_investment, earnest_money, contingency_one_time_costs)
    upfront_project_cost = upfront_project_costs(purchase_price, renovation_cost, earnest_money, total_holding, total_closing, financing_costs)
    cash_invested = calculate_cash_invested(upfront_project_cost, loan_amount)
    cash_on_cash_return = calculate_cash_on_cash_return(total_profit, cash_invested)

    print("\nCalculating user results.....\n")
    print("----------------------------------------------------------------------------------------------------------------- \n")
    print("User information:\n")
    print(f"The purchase price you put in was: ${purchase_price:,.2f}")
    print(f"The renovation cost you put in was: ${renovation_cost:,.2f}")
    print(f"The buying cost you put in was: ${earnest_money:,.2f}")
    print(f"The holding cost you put in was: ${holding_cost:,.2f} per month for {holding_months} months which calculates to ${total_holding:,.2f}")
    print(f"The total closing cost amount is: ${total_closing:,.2f}")
    print(f"The resale value you put in was: ${selling_price:,.2f}")
    print(f"The selling cost percentage you put in was: {selling_costs * 100:.2f}% which calculates to ${total_selling_costs:,.2f}")
    print(f"The loan amount you put in was: ${loan_amount:,.2f} for {loan_months} months at a loan interest rate of {loan_interest * 100:.2f}%")
    print(f"The financing costs we calculated are: ${financing_costs:,.2f}")
    print(f"The contingency/one time costs you put in was: ${contingency_one_time_costs:,.2f}")
    print("----------------------------------------------------------------------------------------------------------------- \n")
    print("Investment and Profit Calculations:\n")
    print(f"Your total investment will be: ${total_investment:,.2f}")
    print(f"Your total profit will be: ${total_profit:,.2f}")
    print(f"Your total upfront project costs will be: ${upfront_project_cost:,.2f}")
    print(f"Your cash invested will be: ${cash_invested:,.2f}")
    print(f"Your Cash-on-Cash Return (COCR) will be: {cash_on_cash_return:.2f}\n")
    print("----------------------------------------------------------------------------------------------------------------- \n")

    # Print profit info
    profit_information = print_profit_info(total_profit, desired_profit, "")
    print(profit_information)

    plot_investment_vs_profit(purchase_price, renovation_cost, holding_cost * holding_months, total_closing, total_investment, total_profit)
    plot_cost_breakdown(purchase_price, renovation_cost, holding_cost * holding_months, total_closing, total_selling_costs, financing_costs)

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("pdf-template.html")

    context = {
        'Name': name, 'Flipping_Address': address, 'State': state,
        'Zip_Code': zip_code, 'Purchase_Price': f"${purchase_price:,.2f}",
        'Renovation_Cost': f"${renovation_cost:,.2f}", 'Earnest_Money': f"${earnest_money:,.2f}",
        'Holding_Cost': f"${holding_cost:,.2f}", 'Holding_Months': holding_months,
        'Total_Holding': f"${total_holding:,.2f}", 'Selling_Price': f"${selling_price:,.2f}",
        'Selling_Costs': f"{selling_costs * 100:.2f}%", 'Total_Selling_Costs': f"${total_selling_costs:,.2f}",
        'Loan_Amount': f"${loan_amount:,.2f}", 'Loan_Months': loan_months,
        'Loan_Interest': f"{loan_interest * 100:.2f}%",
        'Financing_Costs': f"${financing_costs:,.2f}", 'Total_Investment': f"${total_investment:,.2f}",
        'Total_Profit': f"${total_profit:,.2f}", 'Upfront_Project_Costs': f"${upfront_project_cost:,.2f}",
        'Cash_Invested': f"${cash_invested:,.2f}", 'Cash_on_Cash_Return': f"{cash_on_cash_return:.2f}",
        'Desired_Profit': f"${desired_profit:,.2f}", 'Profit_Information': profit_information,
        'Company_Name': company_name, "Total_Closing": f"${float(total_closing):,.2f}",
        'Contingency': f"${contingency_one_time_costs:,.2f}", 'City': city
    }
    print("----------------------------------------------------------------------------------------------------------------- \n")
    print("Relevant Definitions: \n")
    print("Purchase Price: The initial cost of acquiring the property before any renovations or additional expenses.")
    print("Renovation Cost: The total expenditure incurred for all renovation activities on the property.")
    print("Earnest Money: The upfront payment made to secure the property or enter into a contract to purchase the property.")
    print("Holding Costs Per Month: The total expenses associated with holding the property for each month, including mortgage payments, property taxes, insurance, and maintenance costs.")
    print("Closing Cost Percentage: The percentage used to calculate the total closing costs, which include expenses like title charges, transfer taxes, and other miscellaneous costs related to the property transfer.")
    print("Resale Value: The anticipated value of the property after all renovations and improvements have been completed.")
    print("Selling Cost Percentage: The percentage of the property's resale value that will be incurred as fees or expenses associated with selling the property, such as agent commissions and closing costs.")
    print("Loan Information: Details about the loan taken to finance the property, including the loan amount, interest rate, and the duration of the loan.")
    print("Contingency/One-Time Costs: The total amount of expenses that are incurred only once, as well as any additional funds set aside for unexpected or unforeseen costs.")
    print("Desired Profit: The amount of profit that the investor aims to achieve from the sale of the property, after accounting for all expenses and costs.")
    print("----------------------------------------------------------------------------------------------------------------- \n")

    pdf_name = None
    excel_name = None
    email_name = None

    yes_or_no_to_pdf = input("Do you want to print out a pdf version of the results? Y(y) or N(n): ")
    if yes_or_no_to_pdf.lower() == "y":
        pdf_name = input("Enter the pdf name (make sure to include .pdf at the end): ")

    yes_or_no_to_excel = input("Do you want to print out an excel sheet of the results? Y(y) or N(n): ")
    if yes_or_no_to_excel.lower() == "y":
        excel_name = input("Enter the excel sheet name (make sure to include .xlsx at the end): ")

    yes_or_no_to_email = input("Do you want the results to be sent to your email? Y(y) or N(n): ")
    if yes_or_no_to_email.lower() == "y":
        email_name = input("Enter your email address: ")

    # PDF generation
    if pdf_name:
        output_text = template.render(context)
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(output_text, pdf_name, configuration=config)

    # Excel generation
    if excel_name:
        workbook = xlsxwriter.Workbook(excel_name)
        worksheet = workbook.add_worksheet("mainSheet")

        headers = list(context.keys())
        values = list(context.values())

        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        for col, value in enumerate(values):
            worksheet.write(1, col, value)

        def set_column_width(worksheet, col, values):
            length = max(len(str(value)) for value in values)
            worksheet.set_column(col, col, max(10, 2 + length))

        all_values = [headers] + [values]
        for col in range(len(all_values[0])):
            set_column_width(worksheet, col, [row[col] for row in all_values])

        workbook.close()


    # Email sending
    if email_name:
        email_sender = ""
        email_password = ""
        email_receiver = email_name

        subject = "Real Estate Flipping Results"
        body = "Real Estate Flipper Calculator Results\n\n"
        body += f"Name: {name}\n"
        body += f"Flipping Address: {address}\n"
        body += f"State: {state}\n"
        body += f"City: {city}\n"
        body += f"Zip Code: {zip_code}\n\n"
        body += "Your inputs:\n"
        body += f"The purchase price you put in was: ${purchase_price:,.2f}\n"
        body += f"The renovation cost you put in was: ${renovation_cost:,.2f}\n"
        body += f"The total earnest money you put in was: ${earnest_money:,.2f}\n"
        body += f"The holding cost you put in was: ${holding_cost:,.2f} per month for {holding_months} months which calculates to ${total_holding:,.2f}\n"
        body += f"The total closing cost amount is: ${total_closing:,.2f}\n"
        body += f"The resale value you put in was: ${selling_price:,.2f}\n"
        body += f"The selling cost percentage you put in was: {selling_costs * 100:.2f}% which calculates to ${total_selling_costs:,.2f}\n"
        body += f"The loan amount you put in was: ${loan_amount:,.2f} for {loan_months} months at a loan interest rate of {loan_interest * 100:.2f}%\n"
        body += f"The financing costs we calculated are: ${financing_costs:,.2f}\n\n"
        body += "Investment and Profit Calculations:\n"
        body += f"Your total investment will be: ${total_investment:,.2f}\n"
        body += f"Your total profit will be: ${total_profit:,.2f}\n"
        body += f"Your total upfront project costs will be: ${upfront_project_cost:,.2f}\n"
        body += f"Your cash invested will be: ${cash_invested:,.2f}\n"
        body += f"Your Cash-on-Cash Return (COCR) will be: {cash_on_cash_return:.2f}%\n\n"
        body += profit_information
        body+= "\n"
        body += "Relevant Definitions:\n"
        body += "Purchase Price: The initial cost of acquiring the property before any renovations or additional expenses.\n"
        body += "Renovation Cost: The total expenditure incurred for all renovation activities on the property.\n"
        body += "Earnest Money: The upfront payment made to secure the property or enter into a contract to purchase the property.\n"
        body += "Holding Costs Per Month: The total expenses associated with holding the property for each month, including mortgage payments, property taxes, insurance, and maintenance costs.\n"
        body += "Closing Cost Percentage: The percentage used to calculate the total closing costs, which include expenses like title charges, transfer taxes, and other miscellaneous costs related to the property transfer.\n"
        body += "Resale Value: The anticipated value of the property after all renovations and improvements have been completed.\n"
        body += "Selling Cost Percentage: The percentage of the property's resale value that will be incurred as fees or expenses associated with selling the property, such as agent commissions and closing costs.\n"
        body += "Loan Information: Details about the loan taken to finance the property, including the loan amount, interest rate, and the duration of the loan.\n"
        body += "Contingency/One-Time Costs: The total amount of expenses that are incurred only once, as well as any additional funds set aside for unexpected or unforeseen costs.\n"
        body += "Desired Profit: The amount of profit that the investor aims to achieve from the sale of the property, after accounting for all expenses and costs.\n\n"


        em = MIMEMultipart()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject

        em.attach(MIMEText(body, "plain"))

        if pdf_name:
            attach_file_to_email(em, pdf_name)
        if excel_name:
            attach_file_to_email(em, excel_name)

        # Attach the plot images
        attach_file_to_email(em, "investment_vs_profit.png")
        attach_file_to_email(em, "cost_breakdown.png")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        # Remove the images after sending the email
        os.remove("cost_breakdown.png")
        os.remove("investment_vs_profit.png")

    print(
        "----------------------------------------------------------------------------------------------------------------- \n")


# Run the app
if __name__ == '__main__':
    profit_calculations()
