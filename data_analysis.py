import os
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def merge_data():
    # Folder containing all the CSV files
    folder_path = os.getcwd()

    # List to hold dataframes
    dataframes = []

    # Merge all CSV files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            # Read each CSV file
            df = pd.read_csv(file_path)
            dataframes.append(df)

    # Combine all data into one dataframe
    merged_dataframe = pd.concat(dataframes, ignore_index=True)

    # Remove all rows with missing values
    merged_dataframe = merged_dataframe.dropna()

    output_csv = "merged_data_cleaned_exhibition.csv"
    merged_dataframe.to_csv(output_csv, index=False)

def consistancy(decision):
    pivoted_data = merged_dataframe.pivot_table(
        index=['MainAgent', 'TargetAgent'], 
        columns='RunNumber', 
        values=decision, 
        aggfunc='first'  # First ensures that the decision for the same pair is taken (we expect only one decision per run)
        )
    
    # Initialize variables to track consistency
    consistent_pairs = 0
    total_pairs = 0
    overall_probabilities = []

    # Iterate over each pair of MainAgent-TargetAgent
    for _, row in pivoted_data.iterrows():
        # Remove NaN values to only consider runs with decisions
        decisions = row.dropna()
        decision_counts = decisions.value_counts()
        
        # Calculate the probability of the most frequent response
        # Check consistency
        if len(decision_counts) > 0:
            total_pairs += 1
            is_consistent = len(decisions.unique()) <= 1

            most_frequent_count = decision_counts.iloc[0]
            total_count = len(decisions)
            probability = most_frequent_count / total_count
            
            overall_probabilities.append(probability)
            if is_consistent:
                consistent_pairs += 1

    # Calculate average probability across all pairs
    average_probability = sum(overall_probabilities) / len(overall_probabilities) if overall_probabilities else 0
            
    # Calculate overall consistency rate
    consistency_rate = (consistent_pairs / total_pairs) * 100 if total_pairs > 0 else 0
    
    # Print detailed results    
    print(f"\nOverall Consistency for {decision}:")
    print(f"Total Pairs: {total_pairs}")
    print(f"Consistent Pairs: {consistent_pairs}")
    print(f"Consistency Rate: {consistency_rate:.2f}%")
    print(f"Average Probability of Most Frequent Decision: {average_probability:.4f}")

    
    return consistency_rate

def regression(features):
    merged_dataframe['MainAgent'] = merged_dataframe['MainAgent'].astype('category')
    
    # Store results for each RunNumber
    results = {}
    coefficients_per_feature = {feature: [] for feature in features}

    # Perform regression for each RunNumber
    for run_number, run_data in merged_dataframe.groupby('RunNumber'):
        # Define the regression formula
        formula = "Q('Transcript Decision') ~ " + " + ".join([f"Q('{col}')" for col in features]) + " + C(MainAgent)"
        
        # Fit the regression model for this run
        model = smf.ols(formula=formula, data=run_data).fit()
        
        # Save the summary for this RunNumber
        results[run_number] = model.summary()

        for feature in features:
            coefficients_per_feature[feature].append(model.params.get(f"Q('{feature}')", 0))  # Default to 0 if not found

    # Calculate the average coefficient for each feature across the 4 runs
    average_coefficients = {feature: np.mean(coefficients) for feature, coefficients in coefficients_per_feature.items()}

    print("\nAverage coefficients across 4 runs:")
    for feature, avg_coeff in average_coefficients.items():
        print(f"{feature}: {avg_coeff}")

    # Print results for each run
    # for run_number, summary in results.items():
    #     print(f"=== Regression Results for RunNumber {run_number} ===")
    #     print(summary)
    #     print("\n")

def correlation(feature):
    # Calculate positive response rate for each agent within each run
    positive_response_rate = merged_dataframe.groupby(['RunNumber', 'TargetAgent']).apply(
        lambda group: group['Transcript Decision'].sum() / len(group)
    ).reset_index(name='Positive Response Rate')

    # extract the rating of the feature for each agent in each run
    mean_feat = merged_dataframe.groupby(['RunNumber', 'TargetAgent'])[feature].mean().reset_index()

    # Merge the positive response rate with the feature rate
    merged_stats = pd.merge(positive_response_rate, mean_feat, on=['RunNumber', 'TargetAgent'])
    #merged_stats.to_csv('merged'+feature+'.csv', index=False)

    # Calculate the Pearson correlation between positive response rate and Self Reflection Sincerity
    correlation = merged_stats['Positive Response Rate'].corr(merged_stats[feature])

    # Print the result
    print(f"Pearson correlation between Positive Response Rate and {feature}: {correlation}")


def plot_combined_scatter(features):
    # Set up the subplot grid: 2 rows x 3 columns
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
    
    # Flatten axes array for easy indexing
    axes = axes.flatten()
    # Loop through each feature and create a scatter plot with a regression line
    for i, feature in enumerate(features):
        # Calculate positive response rate for each agent within each run
        positive_response_rate = merged_dataframe.groupby(['RunNumber', 'TargetAgent']).apply(
            lambda group: group['Self Reflection Decision'].sum() / len(group)
        ).reset_index(name='Positive Response Rate')

        # Extract the rating of the feature for each agent in each run
        mean_feat = merged_dataframe.groupby(['RunNumber', 'TargetAgent'])[feature].mean().reset_index()

        # Merge the positive response rate with the feature rate
        merged_stats = pd.merge(positive_response_rate, mean_feat, on=['RunNumber', 'TargetAgent'])

        # Calculate the Pearson correlation
        corr = merged_stats['Positive Response Rate'].corr(merged_stats[feature])

        # Plot the scatter plot with regression line
        sns.regplot(
            x='Positive Response Rate', 
            y=feature, 
            data=merged_stats, 
            ax=axes[i],
            scatter_kws={'alpha': 0.5}, 
            line_kws={'color': 'blue'}
        )
        
        # Set title and labels
        axes[i].set_title(f'{feature}\nR = {corr:.3f}', fontsize=14)
        axes[i].set_xlabel('Positive Response Rate', fontsize=12)
        axes[i].set_ylabel(feature, fontsize=12)
    
    # Remove unused axes if features < number of plots
    for j in range(len(features), len(axes)):
        fig.delaxes(axes[j])

    # Save the combined plot as an image
    plt.savefig('combined_scatter_plots_2.png')
    plt.show()


# merge_data()
merged_dataframe = pd.read_csv("merged_data_cleaned_tree.csv")
# print(merged_dataframe['Self Reflection Satisfaction Score'].describe())
features = ["Self Reflection Attractiveness", "Self Reflection Sincerity","Self Reflection Intelligence", 
        "Self Reflection Fun", "Self Reflection Ambition","Self Reflection Shared Interests"]
# features = [
#         "Transcript Ambition", 
#         "Transcript Attractiveness", 
#         "Transcript Fun", 
#         "Transcript Intelligence", 
#         "Transcript Shared Interests", 
#         "Transcript Sincerity"
#     ]
# Map Decision (yes/no) to binary (1/0)

merged_dataframe['Self Reflection Decision'] = merged_dataframe['Self Reflection Decision'].map({'yes': 1, 'no': 0})
merged_dataframe['Transcript Decision'] = merged_dataframe['Transcript Decision'].map({'yes': 1, 'no': 0})
merged_dataframe['High Satisfaction'] = (merged_dataframe['Self Reflection Satisfaction Score'] > 83).astype(int)
#print(merged_dataframe['High Satisfaction'].describe())

# Convert RunNumber to categorical (for easier grouping)
merged_dataframe['RunNumber'] = merged_dataframe['RunNumber'].astype(int)
# plot_combined_scatter(features)


# Subject fixed effect: Add categorical variable for MainAgent
#regression(features)
# for feature in features:
#     correlation(feature)
for decision in ["Self Reflection Decision","Transcript Decision"]:
    consistancy(decision)
