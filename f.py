import os
import shutil
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

class AdvancedBackupManager:
    def __init__(self):
        self.deleted_folder_count = 0
        self.deleted_file_count = 0

    def main(self):
        path = self.select_backup_path()
        days = 30
        threshold_date = datetime.now() - timedelta(days=days)

        if os.path.exists(path):
            for root_folder, folders, files in os.walk(path):
                if threshold_date >= self.get_file_or_folder_age(root_folder):
                    self.remove_folder(root_folder)
                    break
                else:
                    for folder in folders:
                        folder_path = os.path.join(root_folder, folder)
                        if threshold_date >= self.get_file_or_folder_age(folder_path):
                            self.remove_folder(folder_path)

                    for file in files:
                        file_path = os.path.join(root_folder, file)
                        if threshold_date >= self.get_file_or_folder_age(file_path):
                            self.remove_file(file_path)
        else:
            print('Path not found:', path)

        print("Deleted Folders:", self.deleted_folder_count)
        print("Deleted Files:", self.deleted_file_count)

        # Perform regression analysis on the number of deleted files over time
        self.plot_deletion_trend()

    def select_backup_path(self):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askdirectory(title="Select Path to Backup")

    def get_file_or_folder_age(self, path):
        ctime = os.stat(path).st_ctime
        return datetime.fromtimestamp(ctime)

    def remove_folder(self, path):
        try:
            shutil.rmtree(path)
            print('Folder removed successfully:', path)
            self.deleted_folder_count += 1
        except Exception as e:
            print('Unable to remove the folder:', path, '\n', e)

    def remove_file(self, path):
        try:
            os.remove(path)
            print('File removed successfully:', path)
            self.deleted_file_count += 1
        except Exception as e:
            print('Unable to remove the file:', path, '\n', e)

    def plot_deletion_trend(self):
        # Generate some dummy data for illustration
        dates = [datetime.now() - timedelta(days=i) for i in range(10)]
        deleted_files = [2, 5, 8, 12, 18, 22, 27, 32, 40, 45]

        # Perform linear regression
        regression_model = LinearRegression()
        dates_numeric = [date.timestamp() for date in dates]
        dates_numeric_reshaped = np.array(dates_numeric).reshape(-1, 1)
        regression_model.fit(dates_numeric_reshaped, deleted_files)
        predicted_deletions = regression_model.predict(dates_numeric_reshaped)

        # Plot the trend
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=dates, y=deleted_files, label='Actual Deletions')
        sns.lineplot(x=dates, y=predicted_deletions, label='Predicted Deletions', linestyle='dashed')
        plt.title('Deletion Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Deleted Files')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    backup_manager = AdvancedBackupManager()
    backup_manager.main()
