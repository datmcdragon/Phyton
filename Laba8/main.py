""" Main file"""
import pandas as pd
import matplotlib.pyplot as plt

# Функція для завантаження та попередньої обробки даних
def load_and_preprocess(csv_file):
    """ Load file and preprocces info"""
    data = pd.read_csv(csv_file)
    print("Unique values before mapping:", data['radiant_win'].unique())

    # Correct the mapping keys to boolean values
    data['radiant_win'] = data['radiant_win'].map({True: 1, False: 0})
    print("Unique values after mapping:", data['radiant_win'].unique())

    data.dropna(subset=['avg_mmr', 'duration'], inplace=True)

    print(data['avg_mmr'].describe())
    print(data['duration'].describe())
    print(data['avg_mmr'].isnull().sum())
    print(data['duration'].isnull().sum())

    print("Shape of DataFrame after dropna:", data.shape)
    return data

def plot_combined_chart(ax, data):
    """ combination charts"""
    game_counts = data['radiant_win'].value_counts().sort_index()
    avg_mmr_by_result = data.groupby('radiant_win')['avg_mmr'].mean().sort_index()

    print("Game Counts:\n", game_counts)
    print("Average MMR by Result:\n", avg_mmr_by_result)

    ax2 = ax.twinx()

    if not game_counts.empty:
        ax.bar(game_counts.index, game_counts.values, color='blue',
         alpha=0.5, label='Number of Games')
        ax.set_ylim(0, game_counts.values.max() * 1.1)
        ax.set_xticks(game_counts.index)
        ax.set_xticklabels(['Loss', 'Win'])

    if not avg_mmr_by_result.empty:
        ax2.plot(avg_mmr_by_result.index, avg_mmr_by_result.values,
         color='red', marker='o', label='Average MMR')
        ax2.set_ylim(0, avg_mmr_by_result.values.max() * 1.1)

    ax.set_xlabel('Game Result')
    ax.set_ylabel('Number of Games', color='blue')
    ax2.set_ylabel('Average MMR', color='red')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

# Функція для побудови гістограми
def plot_histogram(ax, data, column, title, color):
    """ histogram"""
    ax.hist(data[column], bins=20, color=color, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')

def explore_data(data):
    """ explore data"""
    for column in data.columns:
        # Переконуємося, що стовпець містить числові дані
        if pd.api.types.is_numeric_dtype(data[column]):
            min_value = data[column].min()
            max_value = data[column].max()
            print(f"{column}: Мінімальне значення - {min_value},Максимальне значення - {max_value}")


def main() -> None:
    """ Main method"""
    data = load_and_preprocess('Data/games_cleaned.csv')
    # Дослідження даних
    explore_data(data)

    # Створення фігури з трьома піддіаграмами
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Побудова комбінованого графіка
    plot_combined_chart(axes[0], data)

    # Побудова гістограми середнього MMR
    plot_histogram(axes[1], data, 'avg_mmr', 'Histogram of Average MMR', 'skyblue')

    # Побудова гістограми тривалості ігор
    plot_histogram(axes[2], data, 'duration', 'Histogram of Game Duration', 'salmon')
    # Налаштування загального заголовку
    fig.suptitle('Game Results and Statistics')

    # Налаштування макету та відображення графіків
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)  # Забезпечити місце для загального заголовку
    plt.savefig('Data/game_results_and_statistics.png')
    plt.show()


# Основний блок коду
if __name__ == '__main__':
    main()
