require 'net/http'
require 'json'
require 'uri'

def post_request(url)
  uri = URI(url)
  response = Net::HTTP.get_response(uri)

  # Print response status
  puts "Response status: #{response.code} #{response.message}"

  # Parse body as JSON if possible, otherwise print raw
  begin
    json_body = JSON.parse(response.body)
    puts "Response body:"
    if json_body.empty?
      puts JSON.generate(json_body) # prints {}
    else
      puts JSON.pretty_generate(json_body)
    end
  rescue JSON::ParserError
    puts "Response body:"
    puts response.body
  end
end
