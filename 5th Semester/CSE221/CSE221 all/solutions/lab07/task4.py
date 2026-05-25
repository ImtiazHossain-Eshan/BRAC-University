def minimun_coins(coins, amount):
    arr = [float('inf')] * (amount + 1)
    arr[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            arr[i] = min(arr[i], arr[i - coin] + 1)
    return arr[amount]

input_file = open("input4.txt","r")
output_file = open("output4.txt", "w")
coins_num , amount = map(int, input_file.readline().split())
coins = [int(i) for i in input_file.readline().split()]
output_file.write(f"{minimun_coins(coins, amount)}")