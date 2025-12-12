import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Tracker Pengeluaran Uang",
    layout="wide"
)

# Path file CSV
CSV_FILE = "expenses.csv"

# Fungsi untuk memuat data pengeluaran
@st.cache_data
def load_expenses():
    """Memuat data pengeluaran dari CSV file"""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            st.error(f"Error loading expenses: {e}")
            return pd.DataFrame(columns=['date', 'amount', 'category', 'description'])
    else:
        return pd.DataFrame(columns=['date', 'amount', 'category', 'description'])

# Fungsi untuk menyimpan pengeluaran baru
def save_expense(date, amount, category, description):
    """Menyimpan pengeluaran baru ke CSV"""
    new_expense = pd.DataFrame({
        'date': [date],
        'amount': [amount],
        'category': [category],
        'description': [description]
    })
    
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_expense], ignore_index=True)
    else:
        df = new_expense
    
    df.to_csv(CSV_FILE, index=False)
    st.cache_data.clear()

# Fungsi untuk menghapus pengeluaran
def delete_expense(index):
    """Menghapus pengeluaran berdasarkan index"""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df.drop(index=index).reset_index(drop=True)
        df.to_csv(CSV_FILE, index=False)
        st.cache_data.clear()

# Kategori pengeluaran default
CATEGORIES = [
    "Makanan & Minuman",
    "Transportasi",
    "Belanja",
    "Hiburan",
    "Kesehatan",
    "Pendidikan",
    "Tagihan & Utilitas",
    "Lainnya"
]

# Judul aplikasi
st.title("Tracker Pengeluaran Uang")
st.write("Aplikasi untuk mencatat dan menganalisis pengeluaran keuangan serta memberikan rekomendasi berdasarkan data yang tersedia.")

# Sidebar untuk navigasi dan filter
with st.sidebar:
    st.header("Navigasi")
    page = st.radio(
        "Pilih Halaman",
        ["Tambah Pengeluaran", "Daftar Pengeluaran", "Statistik", "Insights & Saran"]
    )
    
    st.divider()
    st.header("Filter")
    
    # Filter tanggal
    date_filter = st.checkbox("Filter Berdasarkan Tanggal")
    if date_filter:
        date_start = st.date_input("Tanggal Mulai", value=datetime.now().date() - timedelta(days=30))
        date_end = st.date_input("Tanggal Akhir", value=datetime.now().date())
    else:
        date_start = None
        date_end = None
    
    # Filter kategori
    all_categories = ["Semua Kategori"] + CATEGORIES
    selected_category = st.selectbox("Filter Kategori", all_categories)

# Memuat data
df_expenses = load_expenses()

# Filter data berdasarkan pilihan
if not df_expenses.empty:
    df_filtered = df_expenses.copy()
    
    if date_filter and date_start and date_end:
        df_filtered = df_filtered[
            (df_filtered['date'].dt.date >= date_start) &
            (df_filtered['date'].dt.date <= date_end)
        ]
    
    if selected_category != "Semua Kategori":
        df_filtered = df_filtered[df_filtered['category'] == selected_category]
else:
    df_filtered = df_expenses.copy()

# Halaman: Tambah Pengeluaran
if page == "Tambah Pengeluaran":
    st.header("Tambah Pengeluaran Baru")
    
    col1, col2 = st.columns(2)
    
    with col1:
        expense_date = st.date_input("Tanggal", value=datetime.now().date())
        expense_amount = st.number_input("Jumlah (Rp)", min_value=0.0, step=1000.0, format="%.0f")
    
    with col2:
        expense_category = st.selectbox("Kategori", CATEGORIES)
        expense_description = st.text_input("Deskripsi", placeholder="Contoh: Makan siang di restoran")
    
    if st.button("Simpan Pengeluaran", type="primary", use_container_width=True):
        if expense_amount > 0 and expense_description:
            save_expense(expense_date, expense_amount, expense_category, expense_description)
            st.success(f"Pengeluaran sebesar Rp {expense_amount:,.0f} berhasil ditambahkan.")
            st.rerun()
        else:
            st.warning("Mohon lengkapi semua field dengan benar.")

# Halaman: Daftar Pengeluaran
elif page == "Daftar Pengeluaran":
    st.header("Daftar Pengeluaran")
    
    if df_filtered.empty:
        st.info("Belum ada data pengeluaran. Silakan tambah pengeluaran terlebih dahulu.")
    else:
        # Menampilkan summary
        total_spending = df_filtered['amount'].sum()
        st.metric("Total Pengeluaran", f"Rp {total_spending:,.0f}")
        
        # Tabel pengeluaran
        df_display = df_filtered.copy()
        df_display['date'] = df_display['date'].dt.strftime('%d/%m/%Y')
        df_display['amount'] = df_display['amount'].apply(lambda x: f"Rp {x:,.0f}")
        df_display.columns = ['Tanggal', 'Jumlah', 'Kategori', 'Deskripsi']
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Opsi hapus
        st.subheader("Hapus Pengeluaran")
        if not df_filtered.empty:
            delete_index = st.selectbox(
                "Pilih pengeluaran yang akan dihapus",
                range(len(df_filtered)),
                format_func=lambda x: f"{df_filtered.iloc[x]['date'].strftime('%d/%m/%Y')} - {df_filtered.iloc[x]['category']} - Rp {df_filtered.iloc[x]['amount']:,.0f}"
            )
            
            if st.button("Hapus Pengeluaran Terpilih", type="secondary"):
                # Dapatkan index asli dari dataframe yang belum di-filter
                original_index = df_filtered.index[delete_index]
                delete_expense(original_index)
                st.success("Pengeluaran berhasil dihapus.")
                st.rerun()

# Halaman: Statistik
elif page == "Statistik":
    st.header("Statistik Pengeluaran")
    
    if df_filtered.empty:
        st.info("Belum ada data pengeluaran. Silakan tambah pengeluaran terlebih dahulu.")
    else:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_spending = df_filtered['amount'].sum()
        avg_daily = df_filtered.groupby(df_filtered['date'].dt.date)['amount'].sum().mean()
        num_transactions = len(df_filtered)
        avg_transaction = df_filtered['amount'].mean()
        
        with col1:
            st.metric("Total Pengeluaran", f"Rp {total_spending:,.0f}")
        with col2:
            st.metric("Rata-rata Harian", f"Rp {avg_daily:,.0f}")
        with col3:
            st.metric("Jumlah Transaksi", num_transactions)
        with col4:
            st.metric("Rata-rata per Transaksi", f"Rp {avg_transaction:,.0f}")
        
        st.divider()
        
        # Pengeluaran per kategori
        st.subheader("Pengeluaran per Kategori")
        category_summary = df_filtered.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(
                values=category_summary.values,
                names=category_summary.index,
                title="Distribusi Pengeluaran per Kategori"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = px.bar(
                x=category_summary.index,
                y=category_summary.values,
                title="Total Pengeluaran per Kategori",
                labels={'x': 'Kategori', 'y': 'Jumlah (Rp)'}
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        
        # Trend pengeluaran over time
        st.subheader("Trend Pengeluaran")
        daily_spending = df_filtered.groupby(df_filtered['date'].dt.date)['amount'].sum().reset_index()
        daily_spending.columns = ['date', 'amount']
        daily_spending = daily_spending.sort_values('date')
        
        fig_line = px.line(
            daily_spending,
            x='date',
            y='amount',
            title="Pengeluaran Harian",
            labels={'date': 'Tanggal', 'amount': 'Jumlah (Rp)'},
            markers=True
        )
        fig_line.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Tabel summary per kategori
        st.subheader("Ringkasan per Kategori")
        category_stats = df_filtered.groupby('category').agg({
            'amount': ['sum', 'mean', 'count']
        }).round(0)
        category_stats.columns = ['Total', 'Rata-rata', 'Jumlah Transaksi']
        category_stats = category_stats.sort_values('Total', ascending=False)
        category_stats['Total'] = category_stats['Total'].apply(lambda x: f"Rp {x:,.0f}")
        category_stats['Rata-rata'] = category_stats['Rata-rata'].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(category_stats, use_container_width=True)

# Halaman: Insights & Saran
elif page == "Insights & Saran":
    st.header("Insights & Saran Pengeluaran")
    
    if df_filtered.empty:
        st.info("Belum ada data pengeluaran. Silakan tambah pengeluaran terlebih dahulu.")
    else:
        # Analisis pengeluaran
        total_spending = df_filtered['amount'].sum()
        category_summary = df_filtered.groupby('category')['amount'].sum().sort_values(ascending=False)
        top_category = category_summary.index[0] if not category_summary.empty else None
        top_category_amount = category_summary.iloc[0] if not category_summary.empty else 0
        
        # Perbandingan periode
        if len(df_filtered) > 1:
            df_filtered_sorted = df_filtered.sort_values('date')
            first_half = df_filtered_sorted.iloc[:len(df_filtered_sorted)//2]
            second_half = df_filtered_sorted.iloc[len(df_filtered_sorted)//2:]
            
            first_half_total = first_half['amount'].sum()
            second_half_total = second_half['amount'].sum()
            change_percent = ((second_half_total - first_half_total) / first_half_total * 100) if first_half_total > 0 else 0
        else:
            change_percent = 0
        
        # Deteksi spending spike
        daily_spending = df_filtered.groupby(df_filtered['date'].dt.date)['amount'].sum()
        avg_daily = daily_spending.mean()
        std_daily = daily_spending.std()
        spike_threshold = avg_daily + (2 * std_daily) if std_daily > 0 else avg_daily * 2
        spending_spikes = daily_spending[daily_spending > spike_threshold]
        
        # Menampilkan insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Analisis Pengeluaran")
            
            st.info(f"""
            **Total Pengeluaran:** Rp {total_spending:,.0f}
            
            **Kategori Terbesar:** {top_category}
            - Jumlah: Rp {top_category_amount:,.0f}
            - Persentase: {(top_category_amount/total_spending*100):.1f}%
            """)
            
            if len(df_filtered) > 1:
                st.info(f"""
                **Perbandingan Periode:**
                - Periode Pertama: Rp {first_half_total:,.0f}
                - Periode Kedua: Rp {second_half_total:,.0f}
                - Perubahan: {change_percent:+.1f}%
                """)
        
        with col2:
            st.subheader("Saran & Rekomendasi")
            
            # Saran berdasarkan kategori terbesar
            if top_category_amount / total_spending > 0.4:
                st.warning(f"**Perhatian:** Pengeluaran untuk kategori '{top_category}' mencapai {(top_category_amount/total_spending*100):.1f}% dari total pengeluaran. Pertimbangkan untuk mengurangi pengeluaran di kategori ini.")
            
            # Saran berdasarkan trend
            if change_percent > 20:
                st.warning("**Perhatian:** Pengeluaran meningkat lebih dari 20% dibanding periode sebelumnya. Pertimbangkan untuk mengontrol pengeluaran.")
            elif change_percent < -20:
                st.success(f"**Peningkatan:** Pengeluaran menurun {abs(change_percent):.1f}% dibanding periode sebelumnya. Pertimbangkan untuk mempertahankan pola ini.")
            
            # Saran berdasarkan spending spike
            if len(spending_spikes) > 0:
                st.warning(f"**Deteksi:** Terdapat {len(spending_spikes)} hari dengan pengeluaran yang tidak biasa (di atas Rp {spending_spikes.max():,.0f}). Periksa pengeluaran pada hari-hari tersebut.")
            
            # Saran budget
            if len(df_filtered) >= 7:
                weekly_avg = df_filtered.groupby(df_filtered['date'].dt.isocalendar().week)['amount'].sum().mean()
                monthly_budget_suggestion = weekly_avg * 4
                st.info(f"""
                **Saran Budget Bulanan:**
                Berdasarkan rata-rata pengeluaran mingguan (Rp {weekly_avg:,.0f}), 
                disarankan budget bulanan sekitar **Rp {monthly_budget_suggestion:,.0f}**.
                """)
        
        st.divider()
        
        # Visualisasi insights
        st.subheader("Visualisasi Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 5 kategori
            top_5_categories = category_summary.head(5)
            fig_top5 = px.bar(
                x=top_5_categories.values,
                y=top_5_categories.index,
                orientation='h',
                title="Top 5 Kategori Pengeluaran",
                labels={'x': 'Jumlah (Rp)', 'y': 'Kategori'}
            )
            st.plotly_chart(fig_top5, use_container_width=True)
        
        with col2:
            # Spending spikes visualization
            if len(spending_spikes) > 0:
                spike_df = pd.DataFrame({
                    'date': spending_spikes.index,
                    'amount': spending_spikes.values
                })
                fig_spikes = px.bar(
                    spike_df,
                    x='date',
                    y='amount',
                    title="Hari dengan Pengeluaran Tidak Biasa",
                    labels={'date': 'Tanggal', 'amount': 'Jumlah (Rp)'}
                )
                st.plotly_chart(fig_spikes, use_container_width=True)
            else:
                st.info("Tidak ada pengeluaran yang tidak biasa terdeteksi.")
