require 'net/http'
require 'json'
require 'uri'

def post_request(url, body_params = {})
  uri = URI(url)

  # Create HTTP request with headers
  headers = { 'Content-Type' => 'application/json' }
  response = Net::HTTP.post(uri, body_params.to_json, headers)

  # Print response status
  puts "Response status: #{response.code} #{response.message}"

  # Try parsing as JSON
  begin
    json_body = JSON.parse(response.body)
    puts "Response body:"
    puts JSON.pretty_generate(json_body)
  rescue JSON::ParserError
    puts "Response body:"
    puts response.body
  end
end
