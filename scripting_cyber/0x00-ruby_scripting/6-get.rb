def get_request(url)
    require 'net/http'
    response = Net::HTTP.get(URI(url))
    puts response.code
end
