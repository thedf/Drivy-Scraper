function main(splash)
    local host = "proxy.crawlera.com"
    local port = 8010
    local user = "e49ba384b4e94d04bef21798f0bdc5e4"
    local password = ""
    local session_header = "X-Crawlera-Session"
    local session_id = "create"
    splash:on_request(function (request)
        if string.find(request.url, 'doubleclick%.net') or
           string.find(request.url, 'analytics%.google%.com') or
        	 string.find(request.url, 'drivy.imgix.net') or
        	 string.find(request.url, 'googletagmanager.com') or
           string.find(request.url, 'google-analytics.com') or
           string.find(request.url, 'facebook.com')	
        
        
        
        then
            request.abort()
            return
        end

        -- Avoid using Crawlera for subresources fetching to increase crawling
        -- speed. The example below avoids using Crawlera for URLS starting
        -- with 'static.' and the ones ending with '.png'.
        if string.find(request.url, '://static%.') ~= nil or
           string.find(request.url, '%.png$') ~= nil then
            return
        end
        --request:set_header("X-Crawlera-UA", "desktop")
        --request:set_header(session_header, session_id)
        request:set_proxy{host, port, username=user, password=password}
    end)

    splash:on_response_headers(function (response)
        if response.headers[session_header] ~= nil then
            session_id = response.headers[session_header]
        end
    end)

    splash:go(splash.args.url)
	splash:wait(15)

    return splash:html()
end