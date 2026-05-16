import csv
import json
import os
from detector import analyze_input

INPUT_CSV = "data/final_eval.csv"
OUTPUT_CSV = "results/evaluation_results.csv"
METRICS_JSON = "results/metrics_summary.json"

os.makedirs("results", exist_ok=True)

def run_evaluation():
    print("Running evaluation...")

    results = []
    correct = 0
    total = 0

    tp = fp = tn = fn = 0

    with open(INPUT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"].strip()
            expected = row["expected_policy"].strip()
            lang = row.get("language", "en").strip()

            result = analyze_input(
                text=prompt,
                input_id=row["id"],
                user_id="eval_script"
            )

            got = result["decision"]
            match = (got.upper() == expected.upper())
            is_attack = expected.upper() == "BLOCK"
            predicted_attack = got.upper() == "BLOCK"
            if match:
                correct += 1

            total += 1

            is_attack = expected.upper() == "BLOCK"
            predicted_attack = got.upper() == "BLOCK"

            if is_attack and predicted_attack:
                tp += 1
            elif not is_attack and predicted_attack:
                fp += 1
            elif not is_attack and not predicted_attack:
                tn += 1
            elif is_attack and not predicted_attack:
                fn += 1

            results.append({
                "id": row["id"],
                "prompt": prompt[:60],
                "language": lang,
                "expected": expected,
                "got": got,
                "correct": match,
                "rule_score": result.get("rule_score"),
                "semantic_score": result.get("semantic_score"),
                "final_risk": result.get("final_risk"),
                "decision": got
            })

    accuracy = round(correct / total, 4) if total else 0
    precision = round(tp / (tp + fp), 4) if (tp + fp) else 0
    recall = round(tp / (tp + fn), 4) if (tp + fn) else 0
    f1 = round(
        2 * precision * recall / (precision + recall), 4
    ) if (precision + recall) else 0

    metrics = {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn
    }

    with open(OUTPUT_CSV, "w", newline="",
              encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    with open(METRICS_JSON, "w",
              encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n=== RESULTS ===")
    print(f"Total prompts : {total}")
    print(f"Correct       : {correct}")
    print(f"Accuracy      : {accuracy * 100:.1f}%")
    print(f"Precision     : {precision:.4f}")
    print(f"Recall        : {recall:.4f}")
    print(f"F1 Score      : {f1:.4f}")
    print(f"True Positives  : {tp}")
    print(f"False Positives : {fp}")
    print(f"True Negatives  : {tn}")
    print(f"False Negatives : {fn}")
    print(f"\nResults saved to {OUTPUT_CSV}")
    print(f"Metrics saved to {METRICS_JSON}")

if __name__ == "__main__":
    run_evaluation()