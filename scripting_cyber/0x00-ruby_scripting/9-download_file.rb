require 'uri'
require 'open-uri'
require 'fileutils'

if ARGV.length != 2
  puts "Usage: #{$0} URL PATH"
  exit
end

url = ARGV[0]
path = ARGV[1]

begin
    puts "Downloading file from #{url}..."

    # Ensure directory exists
    FileUtils.mkdir_p(File.dirname(path))

    # Open URL and write to local file
    URI.open(url) do |remote_file|
        File.open(path, "wb") do |local_file|
            local_file.write(remote_file.read)
        end
    end

    puts "File downloaded and saved to #{local_path}."
rescue => e
    puts "Error: #{e.message}"
end
