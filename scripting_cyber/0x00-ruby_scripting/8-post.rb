require 'uri'
require 'net/http'
require 'json'

def post_request(url, body_params = {})
    uri = URI(url)

    headers = { 'Content-Type' => 'application/json' }
    res = Net::HTTP.post(uri, body_params.to_json, headers)

    puts "Response status: #{res.code} #{res.message}"

    begin
        json_body = JSON.parse(res.body)
        puts "Response body:"
        puts JSON.pretty_generate(json_body)
    rescue JSON::ParserError
        puts "Response body:"
        puts res.body
    end
end

