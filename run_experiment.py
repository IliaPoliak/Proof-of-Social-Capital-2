import math
import random
import numpy as np

# random.seed(42)
# np.random.seed(42)


STAKE_GINI = 0.9
SC_GINI = 0.75

def experiment(network_size, total_stake, total_sc, sc_value, threshold_function, how_often_threshold_adjusts, blocks_number_to_simulate, scaling_function):
    # Parameters
    print("Parameters:")

    network_size = int(network_size) # int
    print(f"there are {network_size} nodes in the network")

    total_stake = int(total_stake) # int
    print(f"total stake in the network: {total_stake}")

    total_sc = int(total_sc) # int
    print(f"total sc in the network: {total_sc}")

    sc_value = float(sc_value) # float
    print(f"500 social capital cost {sc_value} eth - 1 sc costs {sc_value / 500} eth")
    sc_value = sc_value / 500
    
    threshold_function = threshold_function # k-<int>
    print(f"the function used for threshold calculation is: {threshold_function}")

    how_often_threshold_adjusts = int(how_often_threshold_adjusts) # int
    print(f"the threshold adjusts every {how_often_threshold_adjusts} blocks")

    blocks_number_to_simulate = int(blocks_number_to_simulate) # int
    print(f"the simulation is run with {blocks_number_to_simulate} blocks")

    scaling_function = scaling_function # sqrt, log2
    print(f"scaling function is {scaling_function}")

    print()

    # Derived parameters
    print("Derived parameters:")

    print(f"stake to sc ratio is: x{total_stake / (total_sc * sc_value)}")
    
    num_users_with_sc = int(total_sc / 500)
    print(f"num of nodes with sc: {num_users_with_sc}")

    num_users_with_stake = int(network_size - num_users_with_sc)
    print(f"num of nodes with stake: {num_users_with_stake}")

    print(f"stake_users to sc_users ratio is: x{num_users_with_stake / num_users_with_sc}")


    # Generate users
    users_with_sc = generate_users(num_users_with_sc, total_sc, "sc") # with gini coefficient     
    users_with_stake = generate_users(num_users_with_stake, total_stake, "stake") # randomly
    
    print()
    print(f"Users with SC: {users_with_sc}")
    print(f"Users with Stake: {users_with_stake}")      

    # Join users in one array
    all_users = []
    for sc in users_with_sc:
        all_users.append({"type": "sc", "amount": sc})
    for stake in users_with_stake:
        all_users.append({"type": "stake", "amount": stake})


    sc_threshold = calculate_threshold(threshold_function, total=total_sc*sc_value)
    stake_threshold = calculate_threshold(threshold_function, total=total_stake)
    filtered_users = filter_users(all_users, stake_threshold, sc_threshold, sc_value)
    
    print()
    print(f"Social Capital Threshhod: {sc_threshold} ({sc_threshold / sc_value}) - Stake threshold: {stake_threshold}")
    print()
    print(f"Filtered users:")
    fu = ""
    for user in filtered_users:
        if user["type"] == "stake":
            fu += f"{user["type"]} - {user["amount"]}\n"
        elif user["type"] == "sc":
            fu += f"{user["type"]} - {user["amount"] * sc_value}\n"
    print(fu)

    # Create Blocks
    sc_count = 0
    stake_count = 0
    print("index\taction\t\t\tamount\tblock creator")
    for i in range(blocks_number_to_simulate):

        if not filtered_users:
            raise ValueError("No eligible validators — adjust threshold logic")

        # Select the block creator based on weighted randomness, weight are scaled with scaling function
        w = [scale_stake_or_sc(user["amount"] if user["type"] == "stake" else user["amount"] * sc_value, scaling_function) for user in filtered_users]

        block_creator = random.choices(filtered_users, weights=w, k=1)[0]

        if block_creator["type"] == "sc":
            sc_count += 1
        elif block_creator["type"] == "stake":
            stake_count += 1

        # Create block: 
        x = random.randint(1, 4)
        match x:
            # 1. Register new sc user
            case 1:
                sc_users = [user for user in all_users if user["type"] == "sc"]
                sc_users_values = [user["amount"] for user in sc_users]

                gini = gini_index(sc_users_values)
                
                # choose amount
                amount = random.randint(0, 500)
                amount2 = 500 - amount

                # choose endorsement, weighted
                endorsement = random.choices(sc_users, weights=sc_users_values, k=1)[0]

                # create new user
                all_users.append({"type": "sc", "amount": amount})
                num_users_with_sc += 1

                # handle endorsement
                endorsement["amount"] += amount2

                total_sc += 500
                print(f"{i}:\tnew sc user\t\t{amount}\t{block_creator["type"]}\t\tsc:    {gini}")

            # 2. Endorese another sc user
            case 2:
                sc_users = [user for user in all_users if user["type"] == "sc"]
                sc_users_values = [user["amount"] for user in sc_users]

                gini = gini_index(sc_users_values)
                
                # Choose random endorser
                endorser = random.choice(sc_users)

                if gini < SC_GINI:
                    # Choose weighted endorsment by social capital (increases gini)
                    endorsement = random.choices(sc_users, weights=sc_users_values, k=1)[0]
                else:
                    endorsement = random.choice(sc_users)                    
                                
                # handle endorser
                amount = random.randint(0, endorser["amount"])
                endorser["amount"] -= amount

                # handle endorsement
                endorsement["amount"] += amount

                print(f"{i}:\tnew endorsement\t\t{amount}\t{block_creator["type"]}\t\tsc:    {gini}")

            # 3. Register new stake user
            case 3:
                stake_users = [user for user in all_users if user["type"] == "stake"]
                stake_users_values = [user["amount"] for user in stake_users]

                gini = gini_index(stake_users_values)

                amount = 0
                all_users.append({"type": "stake", "amount": amount})
                total_stake += amount
                num_users_with_stake += 1

                print(f"{i}:\tnew stake user\t\t{amount}\t{block_creator["type"]}\t\tstake: {gini}")

            # 4. Stake some amount of eth
            case 4:
                stake_users = [user for user in all_users if user["type"] == "stake"]
                stake_users_values = [user["amount"] for user in stake_users]

                gini = gini_index(stake_users_values)

                if gini < STAKE_GINI:
                    # choose user (weighted) to icrease gini     
                    staker = random.choices(stake_users, weights=stake_users_values, k=1)[0]
                else:
                    # choose user (randomly) to decrease gini
                    staker = random.choice(stake_users)

                amount = 500 * sc_value
                staker["amount"] += amount
                total_stake += amount
                
                print(f"{i}:\tnew stake\t\t{stake}\t{block_creator["type"]}\t\tstake: {gini}")
        

        # Check i, update threshold and add users to the filtered_users list
        if (i + 1) % how_often_threshold_adjusts == 0:
            sc_threshold = calculate_threshold(threshold_function, total_sc * sc_value)
            stake_threshold = calculate_threshold(threshold_function, total_stake)
            filtered_users = filter_users(all_users, stake_threshold, sc_threshold, sc_value)

            print()
            print(f"Social Capital Threshhod: {sc_threshold} ({sc_threshold / sc_value}) - Stake threshold: {stake_threshold}")
            print(f"Filtered users:\t{len(filtered_users)}")
            fu = ""
            for user in filtered_users:
                if user["type"] == "stake":
                    fu += f"{user["type"]} - {user["amount"]}\n"
                elif user["type"] == "sc":
                    fu += f"{user["type"]} - {user["amount"]} ({user["amount"] * sc_value})\n"
            print(fu)
            if i+1 != blocks_number_to_simulate:
                print("index\taction\t\t\tamount\tblock creator\tgini")


        # remove users that dont pass the threshold every block
        filtered_users = [
            user for user in filtered_users
            if not (
                (user["type"] == "stake" and user["amount"] < stake_threshold) or
                (user["type"] == "sc" and user["amount"] * sc_value < sc_threshold)
            )
        ]

    print()

    print("Checks")

    print(f"stake to sc ratio: {total_stake / (total_sc * sc_value)}")
    print()

    sc_users_values = [user["amount"] for user in all_users if user["type"] == "sc"]
    gini = gini_index(sc_users_values)
    print(f"sc gini: {gini}")

    stake_users_values = [user["amount"] for user in all_users if user["type"] == "stake"]
    gini = gini_index(stake_users_values)
    print(f"stake gini: {gini}")
    print()

    sc_validators = [user["amount"] * sc_value for user in filtered_users if user["type"] == "sc"]
    print(f"Num of SC validators: {len(sc_validators)}")
    print(f"SC validators consensus power sum: {sum(sc_validators)}")
    print()

    stake_validators = [user["amount"] for user in filtered_users if user["type"] == "stake"]
    print(f"Num of Stake validators: {len(stake_validators)}")
    print(f"Stake validators consensus power sum: {sum(stake_validators)}")
    print()



    # Outcomes
    print("Outcomes")

    print(f"Number of blocks created by sc users: {sc_count}")
    print(f"Number of blocks created by stake users: {stake_count}") 

    return (sc_count, stake_count)


def gini_index(arr):    
    
    sorted_arr = sorted(arr)
    
    n = len(arr)
    
    cumulative_sum = 0
    for i, val in enumerate(sorted_arr, start=1):
        cumulative_sum += i * val
    
    total = sum(sorted_arr)
    
    gini = (2 * cumulative_sum) / (n * total) - (n + 1) / n
    
    return gini


def generate_users(number_of_users, total_stake, type):
    if type == "sc":
        inequality = 1.65
        min_gini = SC_GINI - 0.05
        max_gini = SC_GINI + 0.05
    elif type == "stake":
        inequality = 2.5
        min_gini = STAKE_GINI - 0.05
        max_gini = STAKE_GINI + 0.05

    gini = 0
    while True:

        # lognormal distribution, simulates gini inequality
        users = np.random.lognormal(sigma=inequality, size=number_of_users)

        # scale values to sum up to total_stake
        users = users / users.sum() * total_stake

        # convert to integers
        users = users.astype(int).tolist()

        # the sum after conversion is less than total_stake -> fix this
        diff = total_stake - sum(users)

        # distribute the diff
        for i in range(diff):
            users[i] += 1

        gini = gini_index(users)

        # check the gini index
        if min_gini < gini and gini < max_gini:
            return users


def scale_stake_or_sc(num, select):
    match select:
        case "sqrt":
            return math.sqrt(num)
        
        case "log2":
            return math.log2(num + 1)


'''
Threshhold functions evaluation:
all examples are run with: 
20 10 5000 1 <threshold_function> 10 <num_of_blocks> sqrt
random.seed(42)
np.random.seed(42)
   

k - constant
example with k-3 (threshold always equals to 3 eth)
| blocks  | filtered users |
| ------- | -------------- |
| 10      | 1              |
| 100     | 1              |
| 1 000   | 11             |
| 10 000  | 135            |
| 100 000 | 1353           |
problems: for small network there is a big chance of no users to be selected from
for really large networks becomes computationally hard

p - proportional
example with p-100 (threshold = (total_stake or total sc) / 100)
| blocks  | filtered users |
| ------- | -------------- |
| 10      | 19             |    
| 100     | 63             |
| 1 000   | 14             |
| 10 000  | 0              |
| 100 000 | 0              |
problems: starts to scale down where there are too many nodes

c - combined
example with c-3-100 (threshold = min(3, total_stake / 100))
| blocks  | filtered users |
| ------- | -------------- |
| 10      | 19             |             
| 100     | 63             |
| 1 000   | 14             |
| 10 000  | 135            |
| 100 000 | 1353           |
problems: there is a drop in amount of users in the middle we can solve it by adjusting parameters, still too many users for big networks

d - dynamic (my aproach to try to solve the problems above without computationally complex algorithms)
'''
def calculate_threshold(select, total):
    select = select.split("-")  

    match select[0]:
        case "k":
            return int(select[1])
        
        case "p":
            return total / int(select[1])
        
        case "c":
            return min(int(select[1]), total / int(select[2]))
        
        case "d":
            pass            

        

def filter_users(all_users, stake_threshold, sc_threshold, sc_value):
    filtered_users = []
    for user in all_users:
        if (user["type"] == "stake") and (user["amount"] >= stake_threshold):
            filtered_users.append(user)
        elif (user["type"] == "sc") and (user["amount"] * sc_value >= sc_threshold):
            filtered_users.append(user)

    return filtered_users