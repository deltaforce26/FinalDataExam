import io
import matplotlib.pyplot as plt


def create_common_targets_graph(data):
    print("Data received for plotting:", data)

    if not data:
        print("No data available to plot!")
        return None
    group_names = [f"{doc['group_name']} ({doc['target_type']})" for doc in data]
    attack_counts  = [doc['attack_count'] for doc in data]

    plt.figure(figsize=(10, 6))
    plt.barh(group_names, attack_counts, color='skyblue')
    plt.xlabel("Attack Count", fontsize=12)
    plt.ylabel("Group (Target Type)", fontsize=12)
    plt.title("Frequent Attacks by Groups on Target Types", fontsize=14)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return img

