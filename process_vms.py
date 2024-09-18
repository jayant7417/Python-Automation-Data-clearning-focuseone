import os
import pathlib
import pandas as pd

def process_vms_files(folder_path):
    # List to store dataframes
    dataframes = []
    vms_path = folder_path.joinpath('vms')
    print(f"Processing VMS files from: {vms_path}")

    # Loop through all files in the directory
    for filename in os.listdir(vms_path):
        if filename.endswith('.xls'):
            file_path = os.path.join(vms_path, filename)
            try:
                # Attempt to read the file as HTML
                df = pd.read_html(file_path)[0]
                dataframes.append(df)
            except ValueError as e:
                print(f"Error processing file {filename}: {e}")
                continue

    # Concatenate all dataframes
    if dataframes:
        df_vms = pd.concat(dataframes, ignore_index=True)
        df_vms.drop_duplicates(subset=0, inplace=True)
        df_vms[18] = df_vms[18].replace('Hold Request', 'On-Hold')
        df_vms[18] = df_vms[18].replace('Active Request', 'Open')
        df_vms = df_vms[[0, 18]]
        df_vms = df_vms.drop(0).reset_index(drop=True)
        
        output_file_path = folder_path.joinpath('merged', 'vms.csv')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        df_vms.to_csv(output_file_path, index=False)
        print(f"VMS processing done. Output saved to: {output_file_path}")  
        
    else:
        print("No VMS files processed.")

    # Process job board files
    dfs_job = []
    job_board_path = folder_path.joinpath('job board')
    print(f"Processing job board files from: {job_board_path}")

    for filename in os.listdir(job_board_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(job_board_path, filename)
            df = pd.read_csv(file_path)
            df['Source_File'] = filename
            dfs_job.append(df)

    if dfs_job:
        df_job = pd.concat(dfs_job, ignore_index=True)
        df_job['External Job Posting Id'] = df_job['External Job Posting Id'].fillna('')
        replace_patterns = ['(48 hours)', '(48hours)', '(48 hrs)', '(48hrs)', "'",'(48 HOURS)', '(48HOURS)', '(48 HRS)', '(48HRS)','(48 Hours)', '(48Hours)', '(48 Hrs)', '(48Hrs)', "''", '"','()','(',')']
        for pattern in replace_patterns:
            df_job['External Job Posting Id'] = df_job['External Job Posting Id'].str.replace(pattern, '', regex=False)
        
        df_job = df_job.dropna(subset=['Job Status'])
        df_job.drop_duplicates(subset='External Job Posting Id', inplace=True)
        df_job = df_job[['External Job Posting Id', 'Job Status']]
    
        output_file_path = folder_path.joinpath('merged', 'job.csv')#-------------------job
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        df_job.to_csv(output_file_path, index=False)
        print(f"VMS processing done. Output saved to: {output_file_path}")  
    else:
        print("No job board files processed.")
    
    merged_df = pd.merge(df_vms, df_job, left_on=0, right_on='External Job Posting Id', how='outer')
    merged_df = merged_df[[0, 18, 'Job Status']]

    # Drop duplicates based on 'External Job Posting Id'
    merged_df = merged_df.dropna(subset=0)
    merged_df = merged_df.dropna(subset=18)
    merged_df['result'] = merged_df[18] == merged_df['Job Status']
        
    path3 = folder_path.joinpath('do not post','do_not_post_focusone.csv') 
    
    try:
        df3 = pd.read_csv(path3)
    except FileNotFoundError:
        print(f"File not found: {path3}")
        return
        
    posting = merged_df[merged_df['Job Status'].isnull()]
    posting = posting[[0]].astype('int64')
    
    dnt_ids = df3['RequestID'].dropna().astype('int64')
        
    posting = posting[~posting[0].isin(dnt_ids)]

    posting = posting.sort_values(by=0)

    output_file_path = folder_path.joinpath('result', 'Posting.csv')
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    posting.to_csv(output_file_path, index=False)
    print(f"VMS processing done. Output saved to: {output_file_path}")    
    
    status = merged_df.dropna(subset='Job Status')
    #status[0] = status[0].astype('int64')
    status = status[status['result'] == False ]

    status= status.sort_values(by=0)
    
    output_file_path = folder_path.joinpath('result', 'Status.csv')
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    status.to_csv(output_file_path, index=False)
    print(f"VMS processing done. Output saved to: {output_file_path}")


    df_job = df_job[df_job['External Job Posting Id'].astype(str).str.startswith(('1', '2'))]

    output_file_path = folder_path.joinpath('merged', 'job_filter.csv')
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    df_job.to_csv(output_file_path, index=False)
    print(f"VMS processing done. Output saved to: {output_file_path}")  
    


        
    df_job = df_job[(df_job['External Job Posting Id'] != 'Joni Adams') & 
                    (df_job['External Job Posting Id'] != '') & 
                    (df_job['External Job Posting Id'].str.isnumeric())]
    
    df_job = df_job[df_job['Job Status'] != 'Extension']

   
    merged_df1 = pd.merge(df_job, df_vms, left_on='External Job Posting Id', right_on=0, how='outer')
    status1 = merged_df1[['External Job Posting Id', 'Job Status', 0]]
    status1 = status1.dropna(subset=['Job Status'])
    status1 = status1[status1[0].isna()]
    status1= status1.sort_values(by='External Job Posting Id')

    output_file_path = folder_path.joinpath('result', 'Status1.csv')
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    status1.to_csv(output_file_path, index=False)
    print(f"VMS processing done. Output saved to: {output_file_path}")    
    
'''current_directory = os.getcwd()
folder_path = pathlib.Path(current_directory)

process_vms_files(folder_path)'''
