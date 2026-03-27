import sys
import math
import random

# python main.py <network_size> <total_stake> <total_sc> <sc_value> <threshhold_function> <how_often_threshold_adjusts> <blocks_number_to_simulate>

# network_size: int - number of nodes in the network 
# total_stake: int - total eth in stake on the network
# total_sc: int - total sc in stake on the network
# sc_value: float - how much cost 500 sc tokens in eth
# threshhold_function: str - function to be used to calculate threshhold (1/x)
# how_often_threshold_adjusts: int - after whitch amount of blocks the threshhold adjusts
# blocks_number_to_simulate: int - total amount of blocks to create in simulation

# python main.py 20 10 5000 1 1/20 10 1000

def main():
    # Parameters
    print("Parameters:")

    network_size = int(sys.argv[1]) # 10, 100, 1000, 10000
    print(f"there are {network_size} nodes in the network")

    total_stake = int(sys.argv[2]) # int
    print(f"total stake in the network: {total_stake}")

    total_sc = int(sys.argv[3]) # int
    print(f"total sc in the network: {total_sc}")

    sc_value = float(sys.argv[4]) # float
    print(f"500 social capital cost {sc_value} eth - 1 sc costs {sc_value / 500} eth")
    sc_value = sc_value / 500
    
    threshhold_function = sys.argv[5] # 1/x
    print(f"the function used for threshhold calculation is: {threshhold_function}")

    how_often_threshold_adjusts = int(sys.argv[6]) # int
    print(f"the threshhold adjusts every {how_often_threshold_adjusts} blocks")

    blocks_number_to_simulate = int(sys.argv[7]) # int
    print(f"the simulation is run with {blocks_number_to_simulate} blocks")

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
    users_with_sc = generate_users(num_users_with_sc, total_sc) # num_users_with_sc records with numbers from 0 summing up to total_sc     
    users_with_stake = generate_users(num_users_with_stake, total_stake) # num_users_with_stake records with numbers from 0 summing up to total_stake
    
    print()
    print(f"Users with SC: {users_with_sc}")
    print(f"Users with Stake: {users_with_stake}")      

    # Join users in one array
    all_users = []
    for sc in users_with_sc:
        all_users.append({"type": "sc", "amount": sc})
    for stake in users_with_stake:
        all_users.append({"type": "stake", "amount": stake})


    # Filter users
    sc_threshhold = calculate_threshhold(total_sc, threshhold_function)
    stake_threshhold = calculate_threshhold(total_stake, threshhold_function)
    filtered_users = filter_users(all_users, stake_threshhold, sc_threshhold)
    
    print()
    print(f"Social Capital Threshhod: {sc_threshhold} - Stake threshhold: {stake_threshhold}")
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
        w = [scale_stake_or_sc(user["amount"] if user["type"] == "stake" else user["amount"] * sc_value, "sqrt") for user in filtered_users]
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
                all_users.append({"type": "sc", "amount": 500})
                total_sc += 500
                num_users_with_sc += 1
                print(f"{i}:\tnew sc user\t\t{500}")

            # 2. Endorese another sc user
            case 2:
                endorser = random.randint(0, num_users_with_sc - 1)
                endorsement = random.randint(0, num_users_with_sc - 1)
                
                # find endorser
                index = 0
                sc = 0
                for user in all_users:
                    if user["type"] == "sc":
                        if index == endorser:
                            sc = random.randint(0, user["amount"])
                            user["amount"] -= sc
                            break
                        index += 1

                # find endorsement
                index = 0
                for user in all_users:
                    if user["type"] == "sc":
                        if index == endorsement:
                            user["amount"] += sc
                        index += 1

                print(f"{i}:\tnew endorsement\t\t{sc}")

            # 3. Register new stake user
            case 3:
                all_users.append({"type": "stake", "amount": 1})
                total_stake += 1
                num_users_with_stake += 1
                print(f"{i}:\tnew stake user\t\t{1}")

            # 4. Stake some amount of eth
            case 4:
                staker = random.randint(0, num_users_with_stake - 1)
                
                # find staker
                index = 0
                for user in all_users:
                    if user["type"] == "stake":
                        if index == staker:                            
                            stake = random.randint(-user["amount"], user["amount"])
                            user["amount"] += stake
                            break

                        index += 1

                print(f"{i}:\tnew stake\t\t{stake}")
        

        # Check i and update threshhold
        if (i + 1) % how_often_threshold_adjusts == 0:
                sc_threshhold = calculate_threshhold(total_sc, threshhold_function)
                stake_threshhold = calculate_threshhold(total_stake, threshhold_function)
                filtered_users = filter_users(all_users, stake_threshhold, sc_threshhold)

                print()
                print(f"Social Capital Threshhod: {sc_threshhold} - Stake threshhold: {stake_threshhold}")
                print(f"Filtered users:")
                fu = ""
                for user in filtered_users:
                    if user["type"] == "stake":
                        fu += f"{user["type"]} - {user["amount"]}\n"
                    elif user["type"] == "sc":
                        fu += f"{user["type"]} - {user["amount"] * sc_value}\n"
                print(fu)

    print()

    # Outcomes
    print("Outcomes")
    print(f"Number of blocks created by sc users {sc_count}")
    print(f"Number of blocks created by stake users {stake_count}") 


def generate_users(number_of_users, total_stake):
    cut_points = sorted(random.choices(range(0, total_stake+1), k=number_of_users-1))

    arr = [cut_points[0]] 
    
    for i in range(1, len(cut_points)):
        arr.append(cut_points[i] - cut_points[i-1])

    arr.append(total_stake - cut_points[-1])

    return arr


def scale_stake_or_sc(num, select):
    match select:
        case "sqrt":
            return math.sqrt(num)


def calculate_threshhold(num, select):
    if "/" in select:
        return num / int(select[2:])


def filter_users(all_users, stake_threshhold, sc_threshhold):
    filtered_users = []
    for user in all_users:
        if (user["type"] == "stake") and (user["amount"] >= stake_threshhold):
            filtered_users.append(user)
        elif (user["type"] == "sc") and (user["amount"] >= sc_threshhold):
            filtered_users.append(user)

    return filtered_users


if __name__ == "__main__":
    main()
