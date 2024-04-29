# Defining the function for valid customer name
def valid_cstn(cstn):
    if not cstn.isalpha():
        print("Please enter valid name")
        return False
    else:
        return True


# Defining the function for valid product name
def valid_prdtn(prdtn):
    if prdtn not in prdt_prices:
        print("Please enter valid product")
        return False
    else:
        return True


# Defining the function for valid quantity
def valid_qty(qty):
    if not qty.isdigit():
        print("Please enter a valid number of quantity.")
        return False
    else:
        if int(qty) <= 0:
            print("Please enter valid quantity")
            return False
        else:
            return True


# Initializing product prices, customer rewards, and order history
prdt_prices = {"VitaminC": 12.0, "VitaminE": 14.5, "fragrance": 25.0, "vaccine": 32.6, "coldTablet": 6.4}
cstr_rewards = {'Kate': 20, 'Tom': 32}
cstr_order_history = {}


def purchase():
    cstn = input("Please enter customer name: \n")
    while not valid_cstn(cstn):
        cstn = input("Please enter valid customer name: \n")

    products = []
    quantities = []

    # Defining the function for valid product name
    while True:
        product = input("Please enter product name: (type 'done' to finish)\n")
        if product.lower() == 'done':
            break
        if not valid_prdtn(product):
            print("Please enter valid product name.")
            continue
        requires_prescription = product.lower() == "vaccine"
        if requires_prescription:
            while True:
                has_prescription = input(
                    "Does the customer have a doctor's prescription for this product? (y/n):\n").lower()
                if has_prescription == "y":
                    break
                elif has_prescription == "n":
                    print("Sorry: This product requires a doctor's prescription so we can't give you.")
                    return
                else:
                    print("Please enter 'y' if Yes or 'n' if No.")

        products.append(product)

        while True:
            qty = input(f"Enter quantity of {product}: \n")
            if valid_qty(qty):
                quantities.append(int(qty))
                break
            else:
                print("Please enter a valid quantity.\n")

    # Calculate the total price by multiplying the unit price of each product by its quantity,
    # summing up all the individual prices. Then, round the total price to determine the reward points earned.

    total_price = sum(prdt_prices[products[i]] * quantities[i] for i in range(len(products)))
    reward_points = round(total_price)
    discounted_price = [(total_price)-(total_price/100)*10]

    # Check if the customer name is in the customer rewards dictionary and if their accumulated reward points exceed 100.
    # If the condition is met, calculate the discount by dividing the reward points by 100 and multiplying the result by 10.
    # Subtract the discount from the total price and update the customer's reward    if cstn in cstr_rewards and cstr_rewards[cstn] > 100:
    discount = (cstr_rewards[cstn] // 100) * 10
    total_price -= discount
    cstr_rewards[cstn] -= discount

    # Storing the order in customer order history
    order = (products, total_price, reward_points)
    if cstn in cstr_order_history:
        cstr_order_history[cstn].append(order)
    else:
        cstr_order_history[cstn] = [order]

    # Receipt Output
    print("\n*************** Receipt ***************\n")
    print("Customer Name:", cstn)
    for i in range(len(products)):
        product = products[i]
        quantity = quantities[i]
        print("Product:", product)
        print("Unit Price:", prdt_prices[product])
        print("Quantity:", quantity)
        print("-----------------------------------------")
        print("Total Cost: $", total_price)
        print("Discount Price: ", discounted_price)
        print("Earned Reward Points:", reward_points)
        print("Remaining Reward Points:", cstr_rewards[cstn])
    return cstn


# Function to add/update product information
def a_u_products():
    while True:
        prdt_info = input("Enter product information (name price dr_prescription): ").split(',')
        if len(prdt_info) != 3:
            print("Invalid format. Please enter in the format: name price dr_prescription")
            continue
        prdtn = prdt_info[0].strip()
        price = prdt_info[1].strip()
        dr_prescription = prdt_info[2].strip()
        if not price.replace('.', '', 1).isdigit():
            print("Invalid price. Please enter a valid price.")
            continue
        price = float(price)
        if price <= 0:
            print("Invalid price. Please enter a valid positive price.")
            continue
        if dr_prescription.lower() not in ["y", "n"]:
            print("Invalid dr_prescription. Please enter 'y' or 'n'.")
            continue
        prdt_prices[prdtn] = float(price)
        print(f"Product '{prdtn}' added/updated successfully.")
        break
    return


# Function to display existing customers
def exisitng_customer():
    print("The existing customers are", cstr_rewards.keys())
    return


# Function to display existing products
def exisitng_products():
    print("The existing products are", prdt_prices.keys())
    return


# Function to display customer order history
def cst_history():
    cstn = input("Enter the name of the customer: ")
    if cstn not in cstr_rewards:
        print("Customer not found.")
        return

    print("\n***************", cstn, "***************\n")
    orders = cstr_order_history.get(cstn, [])
    if not orders:
        print("No order history found for this customer.")
        return

    print("Order\t\tProducts\t\tTotal Cost\t\tEarned Rewards")
    index = 1
    for order in orders:
        products, total_cost, earned_rewards = order
        print(f"{index}\t\t{', '.join(products)}\t\t{total_cost}\t\t{earned_rewards}")
        index += 1


# Main menu loop
while True:
    print("\n*************** Menu ***************\n")
    print("1. Purchase something")
    print("2. Adding or make changes to the product information")
    print("3. Display existing customers")
    print("4. Display existing products")
    print("5. Display customer order history")
    print("6. Exit")

    options = {
        '1': purchase,
        '2': a_u_products,
        '3': exisitng_customer,
        '4': exisitng_products,
        '5': cst_history,
        '6': lambda: print("Thank you! Please visit again.")
    }

    option = input("Please enter your choice (1-6): ")

    selected_option = options.get(option)
    if selected_option:
        selected_option()
    else:
        print("Invalid choice. Please select an option between 1 and 6.")
