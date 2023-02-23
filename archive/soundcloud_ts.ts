import Soundcloud from "soundcloud.ts"

async function getUser(username, soundcloud) {
    const user = await soundcloud.users.getAlt(username);
    return user;
}

async function getFollowers(username, soundcloud) {
    const followers = await soundcloud.users.followers(username);
    return followers;
}

const soundcloud = new Soundcloud()
const user_result = getUser("chlaer", soundcloud)
// const user_followers = getFollowers("chlaer", soundcloud)
console.log("user result", user_result)
// console.log("user followers", user_followers)

// curl -v 'http://api.soundcloud.com/resolve?url=http://soundcloud.com/chlaer&client_id=VTl9gNS05wF10zfiwKJ6FwK9mJsLVuAV'
// curl -X GET "https://api.soundcloud.com/resolve?url=https%3A%2F%2Fsoundcloud.com%2Fchlaer" -H  "accept: */*"
// curl -X GET 'http://api.soundcloud.com/resolve?url=http://soundcloud.com/chlaer&client_id=VTl9gNS05wF10zfiwKJ6FwK9mJsLVuAV' -H  "accept: */*"
