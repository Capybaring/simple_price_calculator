import streamlit as st
import pandas as pd

# 设置页面配置
st.set_page_config(page_title="物流成本对比计算器", layout="wide")

st.title("🚢 货运方式最优决策分析器")
st.markdown("输入商品参数，系统将自动计算海、陆、空三种方式的总价并选出最优方案。")

# --- 侧边栏：参数配置 ---
st.sidebar.header("核心费率配置 (元)")
rates = {
    "海运": {
        "base": st.sidebar.number_input("海运起步价", value=50),
        "per_kg": st.sidebar.number_input("海运每公斤单价", value=5)
    },
    "陆运": {
        "base": st.sidebar.number_input("陆运起步价", value=30),
        "per_kg": st.sidebar.number_input("陆运每公斤单价", value=12)
    },
    "空运": {
        "base": st.sidebar.number_input("空运起步价", value=100),
        "per_kg": st.sidebar.number_input("空运每公斤单价", value=35)
    }
}

# --- 主页面：数据输入 ---
col1, col2, col3 = st.columns(3)
with col1:
    item_name = st.text_input("商品名称", value="电子零件")
with col2:
    unit_price = st.number_input("商品单价 (元/件)", min_value=0.0, value=200.0)
with col3:
    weight = st.number_input("商品总重量 (kg)", min_value=0.1, value=10.0)

# --- 逻辑计算 ---
base_product_cost = unit_price # 假设这里的单价即为该重量下的总货值
data = []
for mode, price in rates.items():
    shipping_fee = price["base"] + (price["per_kg"] * weight)
    total_all = base_product_cost + shipping_fee
    data.append({
        "运输方式": mode,
        "货值 (元)": base_product_cost,
        "运费 (元)": shipping_fee,
        "总计成本 (元)": total_all
    })

df = pd.DataFrame(data)
df = df.sort_values(by="总计成本 (元)").reset_index(drop=True)

# --- 结果展示 ---
st.subheader("📊 运费对比明细")
# 高亮最优选
st.dataframe(df.style.highlight_min(axis=0, subset=['总计成本 (元)'], color='#D4EDDA'))

# 核心结论卡片
best_option = df.iloc[0]
st.success(f"💡 最优方案推荐：使用 **{best_option['运输方式']}**，预估总成本为 **¥{best_option['总计成本 (元)']:.2f}**")

# 图表展示
st.bar_chart(df.set_index('运输方式')['总计成本 (元)'])