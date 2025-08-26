def get_request(url)
    require 'net/http'
    res = Net::HTTP.get_response(URI(url))
    puts res.code
    puts res.body
end
