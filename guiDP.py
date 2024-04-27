import tkinter as tk
from tkinter import ttk, messagebox

def min_cost_exceed_demand(peak_demand, Prices, watts):
    max_overproduction = 1000  
    n = len(Prices)  
    dp = [(float('inf'),) + (0,) * n for _ in range(peak_demand + max_overproduction + 1)]
    dp[0] = (0,) + (0,) * n

    for i in range(peak_demand + max_overproduction + 1):
        for j in range(n):
            unit_watt = watts[j]
            unit_price = Prices[j]
            if unit_watt <= i:  
                for k in range(1, (peak_demand + max_overproduction) // unit_watt + 1):
                    if i >= k * unit_watt:
                        cost = dp[i - k * unit_watt][0] + k * unit_price
                        if cost < dp[i][0]:
                            new_tuple = list(dp[i - k * unit_watt][1:])
                            new_tuple[j] += k  # 增加當前設備的數量
                            dp[i] = (cost,) + tuple(new_tuple)

    # 找到最小的滿足或超過需求的解
    for i in range(peak_demand, len(dp)):
        if dp[i][0] != float('inf'):
            return (i, dp[i][0]) + dp[i][1:]
    return (None, None) + (None,) * n

def calculate_peak_demand_from_units(monthly_units, conversion_factor):
    # 將每個月的電量轉換為對應的千瓦時
    monthly_kwh = [units * conversion_factor for units in monthly_units]
    # 找出最大的千瓦時作為 peak_demand
    peak_demand = int(max(monthly_kwh))
    return peak_demand

def calculate_button_clicked():
    try:
        # 獲取用戶輸入的12個月的電量
        monthly_units = [float(entry_list[i].get()) for i in range(12)]
        
        # 調用函數計算最大需求量
        peak_demand = calculate_peak_demand_from_units(monthly_units, conversion_factor)
        demand, min_cost, *units = min_cost_exceed_demand(peak_demand, Prices, watts)
        
        # 更新結果顯示
        peak_demand_label.config(text=f"最大需求量：{peak_demand} 千瓦時")
        min_cost_label.config(text=f"最少超過的用電量：{demand} 千瓦時, 最小花費：{min_cost} 元")
        units_label.config(text=f"所需設備數量：{' '.join(f'{units[i]} 台 {unit_labels[i]}' for i in range(len(units)))}")
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的數字")

# 初始化Tkinter窗口
root = tk.Tk()
root.title("電費最小成本計算器")

# 設置窗口大小和初始位置
root.geometry("600x600+600+600")

# 太陽能板和風力發電機的價格和單元發電量
Prices = [40000, 200000, 8000, 90000, 10000]
watts = [1, 2, 5, 7, 10]
unit_labels = ['太陽能板', '風力發電機', '水力發電', '核能發電', '燃煤發電']

# 設置每度電的轉換因子（千瓦時）
conversion_factor = 0.001

# 創建輸入框和標簽
entry_list = []
for i in range(12):
    label = ttk.Label(root, text=f"第 {i+1} 個月用電（度）：")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = ttk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entry_list.append(entry)

# 創建計算按鈕
calculate_button = ttk.Button(root, text="計算", command=calculate_button_clicked)
calculate_button.grid(row=12, column=0, columnspan=2, pady=10)

# 創建結果顯示標簽
peak_demand_label = ttk.Label(root, text="")
peak_demand_label.grid(row=13, column=0, columnspan=2, padx=10, pady=5)

min_cost_label = ttk.Label(root, text="")
min_cost_label.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

units_label = ttk.Label(root, text="")
units_label.grid(row=15, column=0, columnspan=2, padx=10, pady=5)

# 運行窗口主循環
root.mainloop()