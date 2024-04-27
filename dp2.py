# def min_cost_exceed_demand(peak_demand, solar_price, solar_watt, wind_price, wind_watt):
#     # 初始化動態規劃表格，每個元素是一個元組(cost, solar_count, wind_count)
#     # cost 是達到至少這個用電量所需的最小成本
#     # solar_count 是太陽能板的數量，wind_count 是風力發電機的數量
#     dp = [(float('inf'), 0, 0)] * (peak_demand + 1000)  # 假設超出量不超過1000千瓦時
#     dp[0] = (0, 0, 0)  # 沒有需求時不需要花費和組件

#     # 確定每種組件最多可能需要的數量
#     max_solar_needed = (peak_demand + 1000) // solar_watt + 1
#     max_wind_needed = (peak_demand + 1000) // wind_watt + 1

#     # 使用太陽能板和風力發電機填充dp表
#     for i in range(max_solar_needed):
#         for j in range(max_wind_needed):
#             generation = i * solar_watt + j * wind_watt
#             if generation >= len(dp):
#                 continue
#             cost = i * solar_price + j * wind_price
#             if dp[generation][0] > cost:
#                 dp[generation] = (cost, i, j)
    
#     # 從目標需求開始向後找到第一個可實現的解
#     for i in range(peak_demand, len(dp)):
#         if dp[i][0] != float('inf'):
#             # print(dp)
#             return (i, dp[i][0], dp[i][1], dp[i][2])

#     return (None, None, None, None)

def min_cost_exceed_demand(peak_demand, Prices, watts):
    dp = [(float('inf'),) + (0,) * (len(Prices))] * (peak_demand + 1000)  # 假設超出量不超過1000千瓦時
    # 每筆 tuple 的第一個元素是達到至少這個用電量所需的最小成本，其餘元素是再生能源的方案的陣列長度
    dp[0] = (0, 0, 0)  # 沒有需求時不需要花費和組件
    max_need=[]
    for i in range(len(Prices)):
        # 確定每種組件最多可能需要的數量(達成要求只使用單一品項的能源需要的組數)
        max_need.append((peak_demand + 1000) // watts[i])
        print(watts[i],peak_demand,max_need[i])
    print(max_need)# [7,4]
    
    mNeedIndex = 0
    for mNeed in max_need:
        for i in range((mNeed)):
            for j in range((max_need[mNeedIndex+1])):
                generation = i * watts[0] + j * watts[1]
                print("*",generation)
                if generation >= len(dp):
                    continue
                cost = i * Prices[0] + j * Prices[1]
                print(cost)
                if dp[generation][0] >= cost:
                    dp[generation] = (cost, i, j)
        try:
            mNeedIndex += 1
            max_need[mNeedIndex+1]+=0
        except:
            break
        
            
    for i in range(peak_demand, len(dp)):
        if dp[i][0] != float('inf'):
            print(dp)
            return (i, dp[i][0], dp[i][1], dp[i][2])
    return (None, None, None, None)
# 使用提供的數據測試
peak_demand = 1500  # 千瓦時
# solar_price, solar_watt = 40000, 370  # 元/片, 瓦/片
# wind_price, wind_watt = 200000, 800  # 元/台, 瓦/台

Perprice = [40000,20000]
Perwatt = [370,800]
if not(len(Perwatt)==len(Perwatt)):
    print("error")
    exit()
demand, min_cost, solar_units, wind_units = min_cost_exceed_demand(peak_demand, Perprice,Perwatt)
print(f"最少超過的用電量：{demand}千瓦時, 最小花費：{min_cost}元")
print(f"所需太陽能板數量：{solar_units}片, 風力發電機數量：{wind_units}台")