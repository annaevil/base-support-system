//add token in cookie
export function setAuthToken(token: string) {
    document.cookie = `token=${token}; path=/; Secure; HttpOnly`
    // document.cookie = `token=${data.bearer_token}; path=/; samesite=strict`
}

//get token
export function getAuthToken(): string | undefined {
    const matches = document.cookie.match(
        new RegExp('(?:^|; )' + 'token'.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)')
    )
    return matches ? decodeURIComponent(matches[1]) : undefined
}

//remove token
export function removeAuthToken() {
    document.cookie = `token=; path=/; max-age=0`
}