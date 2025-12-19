import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import hashlib

st.set_page_config(page_title="F1 Analytics Dashboard", layout="wide", page_icon="🏎️")

st.markdown("""
    <style>
    .main { background-color: #0b0d10; }
    h1, h2, h3 { color: #ff1801 !important; font-family: 'Arial Black'; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #1f2937; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: #374151; border-radius: 5px; color: white; border: none; padding: 0 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #ef4444 !important; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border-left: 5px solid #ff1801; }
    div[data-testid="stMetricValue"] { color: #10b981; }
    .insight-box { 
        background-color: #1f2937; padding: 15px; border-radius: 8px; 
        border-left: 4px solid #10b981; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ===== ALGORITMA =====

def quick_sort(data, key):
    if len(data) <= 1: return data
    pivot = data[len(data) // 2][key]
    left = [x for x in data if x[key] > pivot]
    middle = [x for x in data if x[key] == pivot]
    right = [x for x in data if x[key] < pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)

def bubble_sort(data, key):
    arr = data.copy()
    for i in range(len(arr)):
        for j in range(0, len(arr)-i-1):
            if arr[j][key] < arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(data, key):
    arr = data.copy()
    for i in range(len(arr)):
        max_idx = i
        for j in range(i+1, len(arr)):
            if arr[j][key] > arr[max_idx][key]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr

def insertion_sort(data, key):
    arr = data.copy()
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j][key] < current[key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

def merge_sort(data, key):
    if len(data) <= 1: return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] >= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def linear_search(data, target_name):
    target_name = target_name.lower()
    for item in data:
        if target_name in item['name'].lower():
            return item
    return None

def binary_search(data, target_name):
    low, high = 0, len(data) - 1
    target_name = target_name.lower()
    while low <= high:
        mid = (low + high) // 2
        if target_name in data[mid]['name'].lower():
            return data[mid]
        elif data[mid]['name'].lower() < target_name:
            low = mid + 1
        else:
            high = mid - 1
    return None

def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def recursive_sum_points(arr):
    if not arr: return 0
    return arr[0] + recursive_sum_points(arr[1:])

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, data):
        if not self.root:
            self.root = Node(data)
        else:
            self._ins(self.root, data)
    
    def _ins(self, node, data):
        if data['points'] < node.data['points']:
            if not node.left:
                node.left = Node(data)
            else:
                self._ins(node.left, data)
        else:
            if not node.right:
                node.right = Node(data)
            else:
                self._ins(node.right, data)
    
    def inorder(self, node, res):
        if node:
            self.inorder(node.left, res)
            res.append(node.data)
            self.inorder(node.right, res)

# ===== DATA LOADER =====

if 'manual_data' not in st.session_state:
    st.session_state.manual_data = []

@st.cache_data
def load_full_data():
    folder = 'archive (1)'
    try:
        results = pd.read_csv(f'{folder}/results.csv', encoding='latin1')
        drivers = pd.read_csv(f'{folder}/drivers.csv', encoding='latin1')
        races = pd.read_csv(f'{folder}/races.csv', encoding='latin1')
        status = pd.read_csv(f'{folder}/status.csv', encoding='latin1')
        constructors = pd.read_csv(f'{folder}/constructors.csv', encoding='latin1')
        
        for df_temp in [results, races, drivers]:
            df_temp.replace(r'\\N', pd.NA, inplace=True)
        
        df = results.merge(drivers[['driverId', 'forename', 'surname', 'nationality']], on='driverId')
        df = df.merge(races[['raceId', 'year', 'name', 'circuitId']], on='raceId')
        df = df.merge(status[['statusId', 'status']], on='statusId')
        df = df.merge(constructors[['constructorId', 'name']], on='constructorId', suffixes=('', '_team'))
        df['full_name'] = df['forename'] + " " + df['surname']
        
        for col in ['points', 'grid', 'positionOrder', 'position']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def load_simple_data():
    df = load_full_data()
    if df is not None:
        simple = df[['driverId', 'full_name', 'points', 'grid', 'year']].copy()
        simple.rename(columns={'full_name': 'name'}, inplace=True)
        agg = simple.groupby(['driverId', 'name']).agg({
            'points': 'sum',
            'grid': 'mean',
            'year': 'count'
        }).reset_index()
        agg.rename(columns={'year': 'laps'}, inplace=True)
        return agg.to_dict('records')
    return []

# ===== MAIN APP =====

st.markdown("<h1 style='text-align: center;'>🏎️ F1 RACE ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Implementasi Struktur Data & Algoritma pada Data Formula 1</p>", unsafe_allow_html=True)

df_full = load_full_data()
data_simple = load_simple_data()

if df_full is None or not data_simple:
    st.error("Dataset tidak ditemukan. Pastikan folder 'archive (1)' tersedia.")
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Sorting", "🔍 Search", "🔐 Hash Table", 
        "🌳 Tree (BST)", "🔄 Recursive", "📥 Input Data"
    ])
    
    # ===== TAB 1: SORTING =====
    with tab1:
        st.subheader("Perbandingan Algoritma Sorting")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_algo = st.selectbox("Pilih Algoritma", [
                "Quick Sort", "Bubble Sort", "Selection Sort", 
                "Insertion Sort", "Merge Sort"
            ])
        with col2:
            sort_metric = st.selectbox("Sort Berdasarkan", ["points", "laps", "grid"])
        
        start_t = time.time()
        sample = data_simple[:100]
        
        if sort_algo == "Quick Sort":
            sorted_data = quick_sort(sample, sort_metric)
        elif sort_algo == "Bubble Sort":
            sorted_data = bubble_sort(sample, sort_metric)
        elif sort_algo == "Selection Sort":
            sorted_data = selection_sort(sample, sort_metric)
        elif sort_algo == "Insertion Sort":
            sorted_data = insertion_sort(sample, sort_metric)
        else:
            sorted_data = merge_sort(sample, sort_metric)
        
        exec_time = (time.time() - start_t) * 1000
        
        with col3:
            st.metric("Execution Time", f"{exec_time:.4f} ms")
        
        chart_df = pd.DataFrame(sorted_data).head(10)
        fig = px.bar(chart_df, x='name', y=sort_metric, 
                     color_discrete_sequence=['#ef4444'],
                     title=f"Top 10 Drivers by {sort_metric.capitalize()}")
        fig.update_layout(template="plotly_dark", 
                         plot_bgcolor='rgba(0,0,0,0)', 
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(chart_df[['name', 'points', 'laps', 'grid']], use_container_width=True)
    
    # ===== TAB 2: SEARCH =====
    with tab2:
        st.subheader("Pencarian Driver dengan Linear & Binary Search")
        
        search_query = st.text_input("Masukkan Nama Driver", placeholder="contoh: Hamilton, Verstappen")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            search_linear = st.button("🔍 Linear Search", use_container_width=True)
        with col_btn2:
            search_binary = st.button("🔍 Binary Search", use_container_width=True)
        
        if search_query and (search_linear or search_binary):
            if search_linear:
                start = time.time()
                result = linear_search(data_simple, search_query)
                time_taken = (time.time() - start) * 1000
                method = "Linear Search"
            else:
                sorted_data = sorted(data_simple, key=lambda x: x['name'])
                start = time.time()
                result = binary_search(sorted_data, search_query)
                time_taken = (time.time() - start) * 1000
                method = "Binary Search"
            
            col_m1, col_m2 = st.columns([3, 1])
            with col_m1:
                if result:
                    st.success(f"✅ Driver ditemukan menggunakan {method}")
                else:
                    st.error(f"❌ Driver tidak ditemukan")
            with col_m2:
                st.metric("Time", f"{time_taken:.4f} ms")
            
            if result:
                st.divider()
                driver_name = result['name']
                driver_id = result['driverId']
                
                driver_df = df_full[df_full['driverId'] == driver_id].copy()
                
                col_v1, col_v2 = st.columns(2)
                
                with col_v1:
                    st.markdown("#### 📊 Performa Poin per Tahun")
                    yearly = driver_df.groupby('year')['points'].sum().reset_index()
                    fig_line = px.line(yearly, x='year', y='points', markers=True)
                    fig_line.update_traces(line_color='#ff1801', line_width=3)
                    fig_line.update_layout(template="plotly_dark")
                    st.plotly_chart(fig_line, use_container_width=True)
                
                with col_v2:
                    st.markdown("#### 🏆 Sirkuit dengan Podium Terbanyak")
                    podium_df = driver_df[driver_df['positionOrder'] <= 3]
                    circuit_podium = podium_df.groupby('name').size().reset_index(name='podiums')
                    circuit_podium = circuit_podium.sort_values('podiums', ascending=False).head(8)
                    
                    fig_bar = px.bar(circuit_podium, x='podiums', y='name', 
                                     orientation='h', color='podiums',
                                     color_continuous_scale='Reds')
                    fig_bar.update_layout(template="plotly_dark", 
                                         yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                col_v3, col_v4 = st.columns(2)
                
                with col_v3:
                    st.markdown("#### 🎯 Distribusi Posisi Finish")
                    pos_dist = driver_df[driver_df['positionOrder'] > 0]['positionOrder'].value_counts().head(10).reset_index()
                    pos_dist.columns = ['position', 'count']
                    fig_pie = px.pie(pos_dist, values='count', names='position', hole=0.4)
                    fig_pie.update_layout(template="plotly_dark")
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col_v4:
                    st.markdown("#### 🏁 Starting Grid vs Finish Position")
                    scatter_df = driver_df[(driver_df['grid'] > 0) & (driver_df['positionOrder'] > 0)].head(50)
                    fig_scatter = px.scatter(scatter_df, x='grid', y='positionOrder',
                                           color='points', size='points',
                                           hover_data=['name', 'year'])
                    fig_scatter.update_layout(template="plotly_dark")
                    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # ===== TAB 3: HASH =====
    with tab3:
        st.subheader("Hash Table & SHA-256 Encryption")
        
        st.markdown("##### Hash Table Visualization (10 Buckets)")
        hash_size = 10
        hash_table = [[] for _ in range(hash_size)]
        
        for d in data_simple[:30]:
            idx = len(d['name']) % hash_size
            hash_table[idx].append(d['name'].split()[-1])
        
        cols = st.columns(5)
        for i in range(hash_size):
            with cols[i % 5]:
                st.markdown(f"**Bucket {i}**")
                if hash_table[i]:
                    st.code("\n".join(hash_table[i][:5]))
                else:
                    st.code("Empty")
        
        st.divider()
        st.markdown("##### SHA-256 Hash Generator")
        
        hash_input = st.text_area(
            "Masukkan teks untuk di-hash:",
            placeholder="contoh: Hamilton akan mengganti mesin di race berikutnya!",
            height=100
        )
        
        if st.button("🔐 Generate Hash"):
            if hash_input:
                hashed = hashlib.sha256(hash_input.encode()).hexdigest()
                st.success("Hash berhasil dibuat!")
                st.code(hashed, language="text")
            else:
                st.warning("Masukkan teks terlebih dahulu")
    
    # ===== TAB 4: TREE =====
    with tab4:
        st.subheader("Binary Search Tree - Driver Rankings")
        
        bst = BST()
        for d in data_simple[:20]:
            bst.insert(d)
        
        tree_result = []
        bst.inorder(bst.root, tree_result)
        
        st.markdown("##### Inorder Traversal (Sorted by Points)")
        tree_df = pd.DataFrame(tree_result[::-1])
        st.dataframe(tree_df[['name', 'points', 'laps']], use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
        <b>Penjelasan:</b> Binary Search Tree digunakan untuk menyimpan data driver 
        berdasarkan poin. Traversal inorder menghasilkan data terurut dari kecil ke besar,
        kemudian dibalik untuk menampilkan ranking tertinggi di atas.
        </div>
        """, unsafe_allow_html=True)
    
    # ===== TAB 5: RECURSIVE =====
    with tab5:
        st.subheader("Algoritma Rekursif")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.markdown("##### Faktorial")
            n_fact = st.number_input("Input N untuk Faktorial", 1, 20, 5, key='fact')
            if st.button("Hitung Faktorial"):
                start = time.time()
                result = factorial(n_fact)
                exec_t = (time.time() - start) * 1000
                st.success(f"Hasil: **{result}**")
                st.info(f"Execution Time: {exec_t:.4f} ms")
        
        with col_r2:
            st.markdown("##### Fibonacci")
            n_fib = st.number_input("Input N untuk Fibonacci", 1, 30, 10, key='fib')
            if st.button("Hitung Fibonacci"):
                start = time.time()
                result = fibonacci(n_fib)
                exec_t = (time.time() - start) * 1000
                st.success(f"Hasil: **{result}**")
                st.info(f"Execution Time: {exec_t:.4f} ms")
        
        st.divider()
        st.markdown("##### Total Poin (Recursive Sum)")
        if st.button("Hitung Total Poin Driver (Top 50)"):
            start = time.time()
            points_list = [d['points'] for d in data_simple[:50]]
            total = recursive_sum_points(points_list)
            exec_t = (time.time() - start) * 1000
            st.success(f"Total Poin: **{total:.2f}**")
            st.info(f"Execution Time: {exec_t:.4f} ms")
    
    # ===== TAB 6: INPUT DATA =====
    with tab6:
        st.subheader("Manual Data Entry - Stack & Queue Implementation")
        
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            input_name = st.text_input("Driver Name", key='input_driver')
        with c2:
            input_time = st.text_input("Lap Time (e.g. 1:30.5)", key='input_time')
        with c3:
            mode = st.radio("Mode", ["Stack", "Queue"], key='mode_select')
        
        if st.button("➕ Add Driver"):
            if input_name and input_time:
                new_entry = {
                    "name": input_name,
                    "laptime": input_time,
                    "timestamp": time.strftime("%H:%M:%S")
                }
                if mode == "Stack":
                    st.session_state.manual_data.insert(0, new_entry)
                else:
                    st.session_state.manual_data.append(new_entry)
                st.success(f"✅ Data ditambahkan via {mode}!")
            else:
                st.warning("⚠️ Mohon isi semua field")
        
        st.divider()
        st.markdown(f"##### Current List (Total: {len(st.session_state.manual_data)})")
        
        if st.session_state.manual_data:
            st.table(pd.DataFrame(st.session_state.manual_data))
            
            col_pull, col_clear = st.columns(2)
            with col_pull:
                if st.button("⬆️ Pull Data (Remove First Item)"):
                    removed = st.session_state.manual_data.pop(0)
                    st.info(f"Pulled: {removed['name']}")
                    st.rerun()
            with col_clear:
                if st.button("🗑️ Clear All Data"):
                    st.session_state.manual_data = []
                    st.rerun()
        else:
            st.info("📭 List kosong. Tambahkan data terlebih dahulu.")

st.sidebar.title("📊 Dashboard Info")
st.sidebar.markdown(f"""
- **Total Drivers:** {len(data_simple)}
- **Total Races:** {df_full['raceId'].nunique() if df_full is not None else 0}
- **Years Covered:** {df_full['year'].min() if df_full is not None else 'N/A'} - {df_full['year'].max() if df_full is not None else 'N/A'}
""")
st.sidebar.divider()
st.sidebar.caption("📌 Data Source: Ergast F1 Database")
st.sidebar.caption("👨‍💻 Developed for PSDA Final Project")