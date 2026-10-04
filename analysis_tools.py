import pandas as pd
from scipy import stats

SCORE_COLUMNS = ["math score", "reading score", "writing score"]
GROUP_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]


def load_data(path="data/students.csv"):
    df = pd.read_csv(path)
    df["average score"] = df[SCORE_COLUMNS].mean(axis=1).round(1)
    return df


def effect_label(eta_squared):
    if eta_squared < 0.01:
        return "negligible"
    if eta_squared < 0.06:
        return "small"
    if eta_squared < 0.14:
        return "medium"
    return "large"


def compare_groups(df, group_col, score_col="average score"):
    groups = [g[score_col].values for _, g in df.groupby(group_col)]
    means = df.groupby(group_col)[score_col].mean().round(1).to_dict()

    if len(groups) == 2:
        p_value = stats.ttest_ind(groups[0], groups[1]).pvalue
    else:
        p_value = stats.f_oneway(*groups).pvalue

    grand_mean = df[score_col].mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = ((df[score_col] - grand_mean) ** 2).sum()
    eta_squared = float(ss_between / ss_total) if ss_total else 0.0

    return {
        "group_column": group_col,
        "score_column": score_col,
        "group_means": means,
        "group_sizes": {
            str(k): int(v) for k, v in df.groupby(group_col).size().items()
        },
        "gap": round(max(means.values()) - min(means.values()), 1),
        "p_value": round(float(p_value), 4),
        "significant": bool(p_value < 0.05),
        "eta_squared": round(eta_squared, 3),
        "effect_size": effect_label(eta_squared),
    }


def find_contradictions(df, group_col):
    by_subject = {}
    means_by_subject = {}
    for subject in SCORE_COLUMNS:
        means = df.groupby(group_col)[subject].mean().round(1)
        means_by_subject[subject] = {str(k): float(v) for k, v in means.items()}
        by_subject[subject] = {
            "top_group": str(means.idxmax()),
            "top_score": float(means.max()),
            "bottom_group": str(means.idxmin()),
            "bottom_score": float(means.min()),
        }

    top_groups = {v["top_group"] for v in by_subject.values()}
    return {
        "group_column": group_col,
        "by_subject": by_subject,
        "means_by_subject": means_by_subject,
        "contradiction": len(top_groups) > 1,
    }


if __name__ == "__main__":
    data = load_data()
    for col in GROUP_COLUMNS:
        result = find_contradictions(data, col)
        print(col, "-> contradiction:", result["contradiction"])
        if result["contradiction"]:
            for subject, info in result["by_subject"].items():
                print(
                    "   ", subject, "top group:", info["top_group"], info["top_score"]
                )
