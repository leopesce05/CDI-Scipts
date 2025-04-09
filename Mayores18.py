import pandas as pd
import matplotlib.pyplot as plt

# Leer los archivos
ratings_df = pd.read_csv('integrated_ratings.csv')
users_df = pd.read_csv('integrated_users.csv')

# Obtener usuarios únicos que han hecho reseñas
usuarios_con_resenas = ratings_df['user_id'].unique()

# Filtrar usuarios que han hecho reseñas en el dataset de usuarios
users_with_ratings = users_df[users_df['user_id'].isin(usuarios_con_resenas)]

# Calcular estadísticas
total_usuarios = len(usuarios_con_resenas)
usuarios_mayores_18 = users_with_ratings[users_with_ratings['age'] > 18]['user_id'].nunique()
usuarios_mayores_igual_18 = users_with_ratings[users_with_ratings['age'] >= 18]['user_id'].nunique()

# Calcular los porcentajes
porcentaje_mayores = (usuarios_mayores_18 / total_usuarios) * 100
porcentaje_mayores_igual = (usuarios_mayores_igual_18 / total_usuarios) * 100

print(f"Total de usuarios que han hecho reseñas: {total_usuarios}")
print(f"Usuarios mayores de 18 años: {usuarios_mayores_18}")
print(f"Porcentaje de usuarios mayores de 18 años: {porcentaje_mayores:.2f}%")
print(f"Usuarios mayores o iguales a 18 años: {usuarios_mayores_igual_18}")
print(f"Porcentaje de usuarios mayores o iguales a 18 años: {porcentaje_mayores_igual:.2f}%")

# Crear un gráfico de torta para mayores o iguales a 18
labels = ['18 años o más', 'Menores de 18 años']
sizes = [porcentaje_mayores_igual, 100 - porcentaje_mayores_igual]
colors = ['#ff9999', '#66b3ff']

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Distribución de usuarios por edad (≥18 años)')
plt.savefig('porcentaje_usuarios_edad.png')
plt.close() 