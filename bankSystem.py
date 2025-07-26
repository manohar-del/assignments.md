from math import ceil

customers = {}
accountCounter = 1  

def generateLoanId(accountNumber):
    prefix = "XYZ"
    accNumStr = str(accountNumber).zfill(6)
    return prefix + accNumStr

def lend(customerId, loanAmount, years, rate):
    global accountCounter
    interest = (loanAmount * years * rate) / 100
    totalAmount = loanAmount + interest
    emi = totalAmount / (years * 12)

    id = generateLoanId(accountCounter)
    accountCounter += 1

    loan = {
        'id': id,
        'loanAmount': loanAmount,
        'years': years,
        'rate': rate,
        'interest': interest,
        'totalAmount': totalAmount,
        'emi': emi,
        'paidAmount': 0,
        'transactions': [],
        'EmiPaid': 0
    }

    customers.setdefault(customerId, {})[id] = loan

    print("\n[LEND] Details:")
    print("Loan ID:", id)
    print("Total Amount:", totalAmount)
    print(f"EMI: {emi:.4f}")
    return id, totalAmount, emi

def payment(customerId, id, amount, mode='EMI'):
    if customerId not in customers:
        print("\nInvalid Customer ID:", customerId)
        return "Loan not found"
    
    if id not in customers[customerId]:
        print("\nInvalid Loan ID:", id)
        return "Loan not found"

    loan = customers[customerId][id]
    loan['transactions'].append({'type': mode, 'amount': amount})
    loan['paidAmount'] += amount

    if mode == 'EMI':
        loan['EmiPaid'] += 1

    print("\n[PAYMENT] Details:")
    print("Received amount:", amount)
    print("Payment mode:", mode)
    print("Loan id:", id)
    return True

def ledger(customerId, id):
    if customerId not in customers:
        print("\nInvalid Customer ID:", customerId)
        return "Loan not found"

    if id not in customers[customerId]:
        print("\nInvalid Loan ID:", id)
        return "Loan not found"

    loan = customers[customerId][id]
    balance = loan['totalAmount'] - loan['paidAmount']
    emiLeft = ceil(balance / loan['emi']) if loan['emi'] else 0

    print("\n[LEDGER] Details for Loan id:", id)
    for txn in loan['transactions']:
        print("Transaction type:", txn['type'])
        print("Transaction amount:", txn['amount'])
        print("---")

    return {
        'id': id,
        'balanceAmount': balance,
        'emiAmount': float(f"{loan['emi']:.4f}"),
        'emiLeft': emiLeft,
        'transactions': loan['transactions']
    }

def display(customerId):
    if customerId not in customers:
        print("\nInvalid Customer ID:", customerId)
        return "Customer not found"

    overview = []
    for id, loan in customers[customerId].items():
        balance = loan['totalAmount'] - loan['paidAmount']
        emiLeft = ceil(balance / loan['emi']) if loan['emi'] else 0

        overview.append({
            'id': id,
            'loanAmount': loan['loanAmount'],
            'totalAmount': loan['totalAmount'],
            'interest': loan['interest'],
            'emi': float(f"{loan['emi']:.4f}"),
            'paidAmount': loan['paidAmount'],
            'emiLeft': emiLeft
        })

    return overview

def bank():
    while True:
        print("\n--- Bank System Menu ---")
        print("1. LEND")
        print("2. PAYMENT")
        print("3. LEDGER")
        print("4. DISPLAY ACCOUNT OVERVIEW")
        print("5. EXIT")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            customerId = input("Enter Customer ID: ")
            loanAmount = float(input("Enter Loan Amount: "))
            years = int(input("Enter Loan Period (Years): "))
            rate = float(input("Enter Rate of Interest: "))
            lend(customerId, loanAmount, years, rate)

        elif choice == '2':
            customerId = input("Enter Customer ID: ")
            id = input("Enter Loan ID: ")
            amount = float(input("Enter Payment Amount: "))
            mode = input("Enter Payment Mode (EMI/lumpSum): ").strip()
            payment(customerId, id, amount, mode)

        elif choice == '3':
            customerId = input("Enter Customer ID: ")
            id = input("Enter Loan ID: ")
            data = ledger(customerId, id)

            if isinstance(data, dict):
                print("\nLEDGER RESULT:")
                print("Loan ID:", data['id'])
                print(f"EMI: {data['emiAmount']:.4f}")
                print("Balance Amount:", data['balanceAmount'])
                print("EMIs Left:", data['emiLeft'])
                print("Transactions:")
                for txn in data['transactions']:
                    print(" -", txn['type'], txn['amount'])

            else:
                print(data)

        elif choice == '4':
            customerId = input("Enter Customer ID: ")
            overview = display(customerId)

            if isinstance(overview, str):
                print(overview)

            else:
                print("\nAccount Overview:")
                for item in overview:
                    print("Loan ID:", item['id'])
                    print("Loan Amount:", item['loanAmount'])
                    print("Total Amount:", item['totalAmount'])
                    print("Interest:", item['interest'])
                    print(f"EMI: {item['emi']:.4f}")
                    print("Amount paid till date:", item['paidAmount'])
                    print("EMIs Left:", item['emiLeft'])
                    print("---")

        elif choice == '5':
            print("Exiting... Thank you!")
            break

        else:
            print("Invalid choice. Try again.")

bank()