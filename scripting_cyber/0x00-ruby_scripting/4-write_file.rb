require 'json'

def merge_json_files(file1_path, file2_path)
  # Read both files
  file1_content = File.read(file1_path)
  file2_content = File.read(file2_path)

  # Parse JSON arrays
  data1 = JSON.parse(file1_content)
  data2 = JSON.parse(file2_content)

  # Merge arrays
  merged_data = data2 + data1

  end
end
