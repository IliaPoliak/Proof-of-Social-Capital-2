import run_experiment
import sys

# python main.py <network_size> <total_stake> <total_sc> <sc_value> <threshold_function> <how_often_threshold_adjusts> <blocks_number_to_simulate> <scaling_function>

# network_size: int - number of nodes in the network 
# total_stake: int - total eth in stake on the network
# total_sc: int - total sc in stake on the network
# sc_value: float - how much cost 500 sc tokens in eth
# threshold_function: str - function to be used to calculate threshold
# how_often_threshold_adjusts: int - after whitch amount of blocks the threshold adjusts
# blocks_number_to_simulate: int - total amount of blocks to create in simulation
# scaling_function: str

# python main.py 1000 500 250_000 1 p-100 10 10 sqrt


def main():
    stake_counts = []
    sc_counts = []

    stake_validators = []
    sc_validators = []

    for _ in range(10):
        (stake_count, sc_count, stake_val, sc_val) = run_experiment.experiment(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
        stake_counts.append(stake_count)
        sc_counts.append(sc_count)
        stake_validators.append(stake_val)
        sc_validators.append(sc_val)

    stake_counts_average = sum(stake_counts) / len(stake_counts)
    sc_counts_average = sum(sc_counts) / len(sc_counts)
        
    stake_validators_average = sum(stake_validators) / len(stake_validators)
    sc_validators_average = sum(sc_validators) / len(sc_validators)

    print()
    print(f"Average Stake count: {stake_counts_average}")
    print(f"Average SC count: {sc_counts_average}")

    print()
    print(f"Average Stake validators count: {stake_validators_average}")
    print(f"Average SC validators count: {sc_validators_average}")


if __name__ == "__main__":
    main()