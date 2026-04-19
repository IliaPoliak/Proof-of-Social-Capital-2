defaulat values are 1000 500 250_000 1 p-100 10 1000 sqrt

stake to sc ratio 50/50
users ratio 50/50

running 10 experiments for each configuration

# Experiments

## Base experiment

| parameters                            | Average Stake Blocks | Average SC Blocks |
| ------------------------------------- | -------------------- | ----------------- |
| 1000 500 250_000 1 p-100 10 1000 sqrt | 535.3                | 464.7             |

## A. Ratios

| ratio | ratio | parameters                            | Average Stake Blocks | Average SC Blocks |
| ----- | ----- | ------------------------------------- | -------------------- | ----------------- |
| 90/10 | x9.0  | 1000 900 50_000 1 p-100 10 1000 sqrt  | 685.9                | 314.1             |
| 80/20 | x4.0  | 1000 800 100_000 1 p-100 10 1000 sqrt | 619.4                | 380.6             |
| 50/50 | x1.0  | 1000 500 250_000 1 p-100 10 1000 sqrt | 535.3                | 464.7             |
| 20/80 | x0.25 | 1000 200 400_000 1 p-100 10 1000 sqrt | 422.1                | 577.9             |
| 10/90 | x0.11 | 1000 100 450_000 1 p-100 10 1000 sqrt | 343.3                | 656.7             |

> the blocks creation ratio is not the same as total power or num of users ration, possible causes
>
> 1. threshhold function - lower threshold barier for minority group adds extra consensus power
> 2. Scaling function - the total power scales so the scaled total power ratio would be different

> with 50/50 ratio sc block still underperforms - possible reason is lower gini coefficient - the users who passed the stake threshhold on average have more consensus power

## B. SC Value experiments

> Instead of adjusting ratio we will now adjust sc value to see if it has the same effect

| sc value | parameters                               | Average Stake Blocks | Average SC Blocks |
| -------- | ---------------------------------------- | -------------------- | ----------------- |
| 0.11     | 1000 500 250_000 0.11 p-100 10 1000 sqrt | 768.2                | 231.8             |
| 0.25     | 1000 500 250_000 0.25 p-100 10 1000 sqrt | 670.9                | 329.1             |
| 1.0      | 1000 500 250_000 1.0 p-100 10 1000 sqrt  | 535.3                | 464.7             |
| 4.0      | 1000 500 250_000 4.0 p-100 10 1000 sqrt  | 379.1                | 620.9             |
| 9.0      | 1000 500 250_000 9.0 p-100 10 1000 sqrt  | 374.5                | 625.5             |

> we can see that the network is adjustable via this parameter

## C. Distribution (same total power ratio 50/50, different number of users ratio)

> the code is adjusted for this experiment to keep the users ratio without changes while running the simulation, when choosing an action weights are calculated based on users ratio not totals ratio

| users ratio   | parameters                            | Average Stake Blocks | Average SC Blocks |
| ------------- | ------------------------------------- | -------------------- | ----------------- |
| 90/10 - x9.0  | 1000 100 50_000 1 p-100 10 1000 sqrt  | 502.0                | 498.0             |
| 80/20 - x4.0  | 1000 200 100_000 1 p-100 10 1000 sqrt | 504.7                | 495.3             |
| 50/50 - x1.0  | 1000 500 250_000 1 p-100 10 1000 sqrt | 535.3                | 464.7             |
| 20/80 - x0.25 | 1000 800 400_000 1 p-100 10 1000 sqrt | 597.9                | 402.1             |
| 10/90 - x0.11 | 1000 900 450_000 1 p-100 10 1000 sqrt | 531.7                | 468.3             |

> no significant difference

## D. Scaling function

| Scaling Function | parameters                            | Average Stake Blocks | Average SC blocks |
| ---------------- | ------------------------------------- | -------------------- | ----------------- |
| sqrt             | 1000 500 250_000 1 p-100 10 1000 sqrt | 535.3                | 464.7             |
| log2             | 1000 500 250_000 1 p-100 10 1000 log2 | 549.6                | 450.4             |
| none             | 1000 500 250_000 1 p-100 10 1000 none | 600.0                | 400               |

without threshold

| Scaling Function | parameters                           | Average Stake Blocks | Average SC blocks |
| ---------------- | ------------------------------------ | -------------------- | ----------------- |
| sqrt             | 1000 500 250_000 1 none 10 1000 sqrt | 364.1                | 635.9             |
| log2             | 1000 500 250_000 1 none 10 1000 log2 | 404.5                | 595.5             |
| none             | 1000 500 250_000 1 none 10 1000 none | 508.1                | 491.9             |

## E. Threshold function

> k-x is constant (x)
> p-y is proportional (total / y)
> c-min-x-y - combined minimum of constant and proporional
> c-max-x-y - combined maximum of constant and proporional
> none - no threshold (0)

| Threshold Function | parameters                                  | Average Stake Blocks  | Average SC blocks     |
| ------------------ | ------------------------------------------- | --------------------- | --------------------- |
| p-20               | 1000 500 250_000 1 p-20 10 1000 sqrt        | 757.4                 | 242.6                 |
| p-50               | 1000 500 250_000 1 p-50 10 1000 sqrt        | 645.4                 | 354.6                 |
| p-100              | 1000 500 250_000 1 p-100 10 1000 sqrt       | 535.3                 | 464.7                 |
| p-200              | 1000 500 250_000 1 p-200 10 1000 sqrt       | 477.2                 | 522.8                 |
| p-500              | 1000 500 250_000 1 p-500 10 1000 sqrt       | 454.0                 | 546.0                 |
| ------------------ | -------------------------------------       | --------------------- | --------------------- |
| k-1                | 1000 500 250_000 1 k-1 10 1000 sqrt         | 560.9                 | 439.1                 |
| k-10               | 1000 500 250_000 1 k-10 10 1000 sqrt        | 605.9                 | 394.1                 |
| k-50               | 1000 500 250_000 1 k-50 10 1000 sqrt        | 790.0                 | 210.0                 |
| k-100              | 1000 500 250_000 1 k-100 10 1000 sqrt       | Error - No Validators | Error - No Validators |
| ------------------ | -------------------------------------       | --------------------- | --------------------- |
| c-min-1-100        | 1000 500 250_000 1 c-min-1-100 10 1000 sqrt | 551.3                 | 448.7                 |
| c-max-1-100        | 1000 500 250_000 1 c-max-1-100 10 1000 sqrt | 551.5                 | 448.5                 |
| none               | 1000 500 250_000 1 none 10 1000 sqrt        | 372.9                 | 627.1                 |

> next I test the validator set size based on network size for selected threshold functions
> I also changed the number of blocks here as this is not important here, it only decreses persicion and slows calculations

| Threshold Function | Network Size | parameters                                       | Av Stake Vals         | Av SC Vals |
| ------------------ | ------------ | ------------------------------------------------ | --------------------- | ---------- |
| p-100              | 100          | 100 50 25_000 1 p-100 10 10 sqrt                 | 14.3                  | 16.6       |
| p-100              | 1_000        | 1_000 500 250_000 1 p-100 10 10 sqrt             | 17.5                  | 20.1       |
| p-100              | 10_000       | 10_000 5_000 2_500_000 1 p-100 10 10 sqrt        | 12.7                  | 3.4        |
| p-100              | 100_000      | 100_000 50_000 25_000_000 1 p-100 10 10 sqrt     | 4.7                   | 0.0        |
| p-100              | 1_000_000    | 1_000_000 500_000 250_000_000 1 p-100 10 10 sqrt | None                  | None       |
| ------------------ | ------------ | --------------------------------------------     | --------------------- | ---------- |
| k-1                | 100          | 100 50 25_000 1 k-1 10 10 sqrt                   | 13.8                  | 10.6       |
| k-1                | 1_000        | 1_000 500 250_000 1 k-1 10 10 sqrt               | 135.7                 | 103.7      |
| k-1                | 10_000       | 10_000 5_000 2_500_000 1 k-1 10 10 sqrt          | 1262.8                | 1029.7     |
| k-1                | 100_000      | 100_000 50_000 25_000_000 1 k-1 10 10 sqrt       | 12093.2               | 10222.2    |
| k-1                | 1_000_000    | 1_000_000 500_000 250_000_000 1 k-1 10 10 sqrt   | 122197.6              | 102602.6   |
| ------------------ | ------------ | --------------------------------------------     | --------------------- | ---------- |
| k-10               | 100          | 100 50 25_000 1 k-10 10 10 sqrt                  | 1.5                   | 1.1        |
| k-10               | 1_000_000    | 1_000_000 500_000 250_000_000 1 k-10 10 10 sqrt  | 7614.3                | 6600.6     |

> The results above show that the proportional function starts to scale down as the network size increases, and constant doesnt scale the number of users at all and they grow proportionally to the network size, witch if the nuber is low creates to many validators for big networks and makes calculations slow and if the number is too high makes small networks centralized.

> We can solve this by adjusting the combined treshold function choosing the minimal of proporional and constant, selecting lower threshold from proportional function and higher for constant.

| Threshold Function | Network Size | parameters                                              | Av Stake Vals | Av SC Vals |
| ------------------ | ------------ | ------------------------------------------------------- | ------------- | ---------- |
| p-100              | 1_000        | 1_000 500 250_000 1 p-100 10 10 sqrt                    | 17.5          | 20.1       |
| p-100              | 10_000       | 10_000 5_000 2_500_000 1 p-100 10 10 sqrt               | 12.7          | 3.4        |
| ------------------ | ------------ | --------------------------------------------            | ------------- | ---------- |
| k-10               | 10_000       | 10_000 5_000 2_500_000 1 k-10 10 10 sqrt                | 77.4          | 65.3       |
| k-20               | 10_000       | 10_000 5_000 2_500_000 1 k-20 10 10 sqrt                | 38.9          | 19.4       |
| ------------------ | ------------ | --------------------------------------------            | ------------- | ---------- |
| c-min-20-100       | 100          | 100 50 25_000 1 c-min-20-100 10 10 sqrt                 | 12.6          | 16.0       |
| c-min-20-100       | 1_000        | 1_000 500 250_000 1 c-min-20-100 10 10 sqrt             | 15.1          | 18.1       |
| c-min-20-100       | 10_000       | 10_000 5_000 2_500_000 1 c-min-20-100 10 10 sqrt        | 34.0          | 19.5       |
| c-min-20-100       | 100_000      | 100_000 50_000 25_000_000 1 c-min-20-100 10 10 sqrt     | 348.6         | 208.6      |
| c-min-20-100       | 1_000_000    | 1_000_000 500_000 250_000_000 1 c-min-20-100 10 10 sqrt | 3551.7        | 2073.3     |

> this is a good result small networks have enough validators and big networks dont have too much, the transition is smooth

## Final Experiment

| parameters                                           | Average Stake Blocks | Average SC Blocks |
| ---------------------------------------------------- | -------------------- | ----------------- |
| 1_000 500 250_000 1 c-min-20-100 10 1_000 sqrt       | 499.5                | 500.5             |
| 10_000 5_000 2_500_000 1 c-min-20-100 10 10_000 sqrt | 6303                 | 3697              |
