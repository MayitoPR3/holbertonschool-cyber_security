require 'json'

def count_user_ids(path)
  # Read file content
  file_content = File.read(path)
  
  # Parse JSON into Ruby objects (usually an array of hashes)
  data = JSON.parse(file_content)
  
  # Count occurrences of each userId
  counts = Hash.new(0)
  data.each do |item|
    counts[item["userId"]] += 1
  end

  # Print results in sorted order by userId
  counts.sort.each do |user_id, count|
    puts "#{user_id}: #{count}"
  end
end
