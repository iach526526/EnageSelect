def min_cost(peak_demand, Prices, watts,overload=0):
    n = len(Prices)  # 發電設備種類
    dp = [(float('inf'),) + (0,) * n for _ in range(peak_demand + overload + 1)]
    dp[0] = (0,) + (0,) * n

    for i in range(peak_demand + overload + 1):
        for j in range(n):
            unit_watt = watts[j]
            unit_price = Prices[j]
            if unit_watt <= i:  
                #當前設備的單位發電量不超過需要考慮的發電量
                for k in range(1, (peak_demand + overload) // unit_watt + 1):
                    if i >= k * unit_watt:
                        cost = dp[i - k * unit_watt][0] + k * unit_price
                        if cost < dp[i][0]:
                            new_tuple = list(dp[i - k * unit_watt][1:])
                            new_tuple[j] += k  # 增加當前設備的數量
                            dp[i] = (cost,) + tuple(new_tuple)

    #找出能量剛好滿足或超過需求最少、且最便宜的最佳解
    for i in range(peak_demand, len(dp)):
        if dp[i][0] != float('inf'):
            return (i, dp[i][0]) + dp[i][1:]
    return (None, None) + (None,) * n


peak_demand = 14  # 千瓦时需求
overload = 1000  # 最大可容忍超出量，誤差值
Prices = [40000, 200000,8000,90000,1000000]  # 每個設施單位成本（權重）
watts = [1,2,5,7,100]  # 每個設施單位發電量
unit_labels = ['太陽能板', '風力', '水利', '廚餘', '核能'] 
Prices[0]#對應到watts[0]，Prices[1]對應到watts[1]，以此類推

#自訂輸入
# Prices =[]
# watts = []
# unit_labels = []
# n=int(input("輸入發電方式數量"))
# peak_demand , overload= map(int,input("最大用電量、可容許超出能量").split(" "))
# for i in range(n):
#     unit_labels.append(input("輸入發電方式名稱"))
#     Prices.append(int(input(f"輸入 {unit_labels[i]} 價格")))
#     watts.append(int(input(f"輸入 {unit_labels[i]} 發電量")))


demand, min_cost, *units = min_cost(peak_demand, Prices, watts,overload)
output_details = ", ".join(f"{units[i]}（單位）{unit_labels[i]}" for i in range(len(units)))

print(f"產生最少超過需求的電量:{demand}千瓦时, 最小花費：{min_cost}元")
print(f"所需設備：{output_details}")
