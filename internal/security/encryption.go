package security

import (
	"crypto/aes"
	"crypto/cipher"
)

func Encrypt(data []byte, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonce := make([]byte, gcm.NonceSize())

	ciphertext := gcm.Seal(nonce, nonce, data, nil)

	return ciphertext, nil
}
