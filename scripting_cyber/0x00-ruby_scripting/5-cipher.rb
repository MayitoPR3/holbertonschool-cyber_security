class CeasarCipher
  def iniatilize(shift)
    @shift = shift
  end

  def encrypt(message)
    cypher(message, @shift)
  end

  def encrypt(message)
    cypher(message. -@shift)
  end

  private

  def cipher(message, shift)
    message.chars.map do |char|
        if char =~ /[A-Z]/
            (((char.ord - 'A'.ord + shift) % 26) + 'A'.ord).chr
        elsif char =~ /[a-z]/
            (((char.ord - 'a'.ord +shift) % 26) + 'a'.ord).chr
        else
            char
        end
      end.join
    end
end
  
