#!/bin/env ruby
require 'puppeteer-ruby'

launch_options = {
  executable_path: `which chromium`.chomp,
  args: ['--no-sandbox'],
  headless: false
}
Puppeteer.launch(**launch_options) do |browser|
  page = browser.pages.first || browser.new_page
  page.viewport = Puppeteer::Viewport.new(width: 1024, height: 800, device_scale_factor: 1.5)

  page.goto("https://ec.europa.eu/taxation_customs/vies/?locale=pl")

  page.click(".wt-cck-btn-add")

  page.select('select[name="memberStateCode"]', "IE")
  page.select('select[name="requesterMemberStateCode"]', "IE")
  page.type_text('input[name="number"]', "xyz")
  page.type_text('input[name="requesterNumber"]', "xyz")

  page.wait_for_navigation do
    page.click("#submit")
  end

  page.screenshot(path: "1.capture_a_site_chromium.png")
end