# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import json
import urllib

class DevToTopArticles(kp.Plugin):
    """
    Shows the top 10 articles on Dev.to
    """

    ITEMCAT_READ = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_RESULT = kp.ItemCategory.USER_BASE + 2

    API_URL = "https://dev.to/api/articles?top=1&per_page=10"
    API_USER_AGENT = "Mozilla/5.0"

    ACTION_OPEN_URL = "open_url"
    ACTION_COPY_URL = "copy_url"

    def __init__(self):
        super().__init__()

    def on_start(self):
        self.logo = 'res://%s/%s'%(self.package_full_name(),'devto.png')
        actions = [
            self.create_action(
                name=self.ACTION_OPEN_URL,
                label="Read",
                short_desc="Opens the article in a browser"
            ),
            self.create_action(
                name=self.ACTION_COPY_URL,
                label="Copy URL",
                short_desc="Copy result URL to clipboard"
            )]
        self.set_actions(self.ITEMCAT_RESULT, actions)
        pass

    def on_catalog(self):
        catalog = []
        
        catalog.append(self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label="devto",
            short_desc="View top 10 articles on dev.to",
            target='devto',
            icon_handle=self.load_icon(self.logo),
            args_hint=kp.ItemArgsHint.REQUIRED,
            hit_hint=kp.ItemHitHint.NOARGS))

        self.set_catalog(catalog)
        pass

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != kp.ItemCategory.KEYWORD:
            return
        
        request = urllib.request.Request(self.API_URL)
        request.add_header("User-Agent", self.API_USER_AGENT)
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read())

        suggestions = []
        for d in data:
            suggestions.append(self.create_item(
                category=self.ITEMCAT_RESULT,
                label=d['title'],
                short_desc=d['description'],
                target=d['url'],
                icon_handle=self.load_icon(self.logo),
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE))
        
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)
        pass

    def on_execute(self, item, action):
        kpu.web_browser_command(
            url = item.target(),
            execute = True
        )
        pass

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass
