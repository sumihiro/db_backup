import yaml
import os
import subprocess
from datetime import datetime, timedelta

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def create_backup_directory(base_dir, host, database):
    backup_dir = os.path.join(base_dir, 'backup', host, database)
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir

def backup_database(host, database, user, password, backup_dir):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}.sql"
    backup_path = os.path.join(backup_dir, filename)
    
    command = f"mysqldump -h {host} -u {user} -p{password} {database} > {backup_path}"
    subprocess.run(command, shell=True, check=True)

def remove_old_backups(backup_dir, retention_days):
    today = datetime.now().date()
    print(f"削除対象のバックアップディレクトリ: {backup_dir}")
    print(f"保持する日数: {retention_days}日")
    
    for file in os.listdir(backup_dir):
        if file.endswith('.sql'):
            file_path = os.path.join(backup_dir, file)
            try:
                file_date = datetime.strptime(file.split('.')[0], '%Y-%m-%d').date()
                age_days = (today - file_date).days
                print(f"ファイル: {file}, 作成日: {file_date}, 経過日数: {age_days}日")
                if age_days >= retention_days:
                    os.remove(file_path)
                    print(f"削除されたファイル: {file_path}")
            except ValueError:
                print(f"無効なファイル名形式: {file}")

def main():
    config = load_config()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for db in config['databases']:
        backup_dir = create_backup_directory(base_dir, db['host'], db['database'])
        backup_database(db['host'], db['database'], db['user'], db['password'], backup_dir)
        remove_old_backups(backup_dir, config['retention_days'])

if __name__ == "__main__":
    main()

