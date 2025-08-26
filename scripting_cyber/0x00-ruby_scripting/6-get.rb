def get_request(url)
    require 'net/http'
    uri = URI(url)
    response = Net::HTTP.get(uri)
    puts response
end
