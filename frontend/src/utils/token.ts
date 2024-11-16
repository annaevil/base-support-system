//add token in cookie
export function setAuthToken(token: string) {
    document.cookie = `token=${encodeURIComponent(token)}; path=/; Secure; HttpOnly`
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