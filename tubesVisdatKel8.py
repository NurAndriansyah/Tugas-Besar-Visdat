# Import library yang dibutuhkan
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# --- Memuat dataset Netflix ---
file_path = 'Netflix_movies_and_tv_shows_clustering.csv'
netflix_data = pd.read_csv(file_path)

# --- Bagian 1: Distribusi Genre ---
genre_counts = netflix_data['listed_in'].str.split(', ').explode().value_counts()
genre_counts_df = genre_counts.reset_index()
genre_counts_df.columns = ['Genre', 'Count']
genre_counts_df = genre_counts_df.sort_values('Count', ascending=False).reset_index(drop=True)

# --- Streamlit App ---
st.title("Analisis Konten Netflix")

# Distribusi Genre Netflix
st.header("1. Distribusi Genre Netflix")
fig_genre = px.bar(
    genre_counts_df,
    x='Count',
    y='Genre',
    orientation='h',
    title="Distribusi Genre Netflix",
    labels={'Count': 'Jumlah Konten', 'Genre': 'Genre'},
    color_discrete_sequence=["skyblue"],
)
st.plotly_chart(fig_genre, use_container_width=True)

# --- Bagian Baru: Perbandingan Film dan TV Show ---
st.header("2. Perbandingan Film dan TV Show di Netflix")
st.write("Visualisasi ini membandingkan jumlah konten berdasarkan tipe (Film atau TV Show).")

# Hitung jumlah Film dan TV Show
type_counts = netflix_data['type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']  # Ubah nama kolom

# Membuat grafik batang
fig_type = px.bar(
    type_counts,
    x='Type',
    y='Count',
    color='Type',
    title="Perbandingan Film dan TV Show di Netflix",
    labels={'Type': 'Tipe Konten', 'Count': 'Jumlah Konten'},
    color_discrete_map={'Movie': 'blue', 'TV Show': 'green'},  # Warna khusus
)

fig_type.update_layout(
    xaxis=dict(title="Tipe Konten"),
    yaxis=dict(title="Jumlah Konten"),
    height=400,
    margin=dict(l=50, r=50, t=50, b=50)
)

# Tampilkan grafik
st.plotly_chart(fig_type, use_container_width=True)

# --- Bagian 3: Distribusi Konten Berdasarkan Negara ---
st.header("3. Distribusi Konten Netflix Berdasarkan Negara")
st.write("Visualisasi peta dunia menunjukkan jumlah konten berdasarkan negara asal.")
selected_genre = st.selectbox("Pilih Genre (Opsional)", options=["Semua"] + genre_counts_df['Genre'].tolist())
if selected_genre == "Semua":
    country_counts = netflix_data['country'].value_counts().reset_index()
else:
    filtered_data = netflix_data[netflix_data['listed_in'].str.contains(selected_genre, na=False)]
    country_counts = filtered_data['country'].value_counts().reset_index()
country_counts.columns = ['Country', 'Count']
if country_counts.empty:
    st.write("Tidak ada data yang sesuai dengan genre yang dipilih.")
else:
    fig_country = px.choropleth(
        country_counts,
        locations='Country',
        locationmode='country names',
        color='Count',
        color_continuous_scale='Viridis',
        title='Distribusi Konten Netflix Berdasarkan Negara',
        labels={'Count': 'Jumlah Konten'}
    )
    st.plotly_chart(fig_country, use_container_width=True)

# --- Bagian 4: Pertumbuhan Konten Berdasarkan Tahun ---
st.header("4. Pertumbuhan Jumlah Film/TV Show Netflix")
st.write("Visualisasi ini menunjukkan pertumbuhan jumlah film dan acara TV berdasarkan tahun rilis.")
release_year_counts = netflix_data['release_year'].value_counts().sort_index()
release_year_df = release_year_counts.reset_index()
release_year_df.columns = ['Release Year', 'Count']
release_year_df = release_year_df.sort_values('Release Year')
selected_year = st.slider(
    "Pilih Tahun Rilis",
    int(release_year_df['Release Year'].min()),
    int(release_year_df['Release Year'].max()),
    (int(release_year_df['Release Year'].min()), int(release_year_df['Release Year'].max()))
)
filtered_year_df = release_year_df[
    (release_year_df['Release Year'] >= selected_year[0]) &
    (release_year_df['Release Year'] <= selected_year[1])
]
chart_year = alt.Chart(filtered_year_df).mark_line(point=True).encode(
    x='Release Year:O',
    y='Count:Q',
    tooltip=['Release Year', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_year, use_container_width=True)

# --- Bagian 5: Distribusi Konten Berdasarkan Rating ---
st.header("5. Distribusi Konten Berdasarkan Rating")
rating_counts = netflix_data['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']
fig_rating = px.bar(
    rating_counts,
    x='Rating',
    y='Count',
    color='Count',
    color_continuous_scale='viridis',
    title="Distribusi Konten Berdasarkan Rating",
    labels={'Count': 'Jumlah Konten', 'Rating': 'Rating'}
)
fig_rating.update_layout(
    xaxis=dict(title="Rating"),
    yaxis=dict(title="Jumlah Konten"),
    height=500,
    margin=dict(l=50, r=50, t=50, b=50)
)
st.plotly_chart(fig_rating, use_container_width=True)
