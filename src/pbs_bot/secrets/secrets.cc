#include "secrets.h"

std::string encrypt_slack_token(std::string token, std::string key) {
    std::string encrypted_token = token;

    for (size_t i = 0; i < token.size(); ++i) {
        encrypted_token[i] = token[i] ^ key[i % key.size()];
    }
    return encrypted_token;
}

std::string decrypt_slack_token(std::string token, std::string key) {
    return encrypt_slack_token(token, key);
}