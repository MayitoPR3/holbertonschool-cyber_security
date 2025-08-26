require 'net/http'
require 'json'
require 'uri'

def get_request(url)
    uri = URI(url)
    response = Net::HTTP.get(uri)

    puts "Response status: #{response.code} #{response.message}"

    begin
        json_body = JSON.parse(response.body)
        puts "Response body:"
        puts JSON.pretty_generate(json_body)
    rescue JSON::ParserError
        puts "Response body:"
        puts response.body
    end
end
