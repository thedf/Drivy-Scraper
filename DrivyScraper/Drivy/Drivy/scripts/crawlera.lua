-- myscript.lua
function main(splash)
    -- begin example from crawlera docs
    local host = "proxy.crawlera.com"
    local port = 8010
    local user = splash.args.apikey
    local password = ""
    local session_header = "X-Crawlera-Session"
    local session_id = "create"

    splash:on_request(function (request)
        --request:set_header("X-Crawlera-UA", "desktop")
        request:set_header(session_header, session_id)
        request:set_proxy{host, port, username=user, password=password}
        request:set_header('X-Crawlera-Timeout', 40000)
    end)

    splash:on_response_headers(function (response)
        if response.headers[session_header] ~= nil then
            session_id = response.headers[session_header]
        end
    end)
    -- end example from crawlera docs

    -- customized render script inspired by scrapy-splash examples
    splash:init_cookies(splash.args.cookies)
    assert(splash:go{
        splash.args.url,
        headers=splash.args.headers,
        http_method=splash.args.http_method,
        body=splash.args.body,
    })
    assert(splash:wait(0.5))

    local entries = splash:history()
    local last_response = entries[#entries].response
    return {
        url = splash:url(),
        headers = last_response.headers,
        http_status = last_response.status,
        cookies = splash:get_cookies(),
        html = splash:html(),
    }
end