#!/usr/bin/env python3
"""
notify.py — emails Khalil the URLs of everything the bot just made.

Gmail SMTP. You need an APP PASSWORD, not your normal account password:
  myaccount.google.com > Security > 2-Step Verification > App passwords
Store it as a masked, protected CI variable named SMTP_PASS.
"""

import datetime as dt
import os
import smtplib
from email.message import EmailMessage

TO = os.environ.get("NOTIFY_TO", "engrkhalil77@gmail.com")


def render(results):
    today = dt.date.today().strftime("%d %B %Y")
    drafts = [r for r in results if r["state"].startswith("DRAFT")]

    rows = ""
    for r in results:
        colour = "#F59E0B" if r["state"].startswith("DRAFT") else "#0c4a45"
        rows += f"""
        <tr>
          <td style="padding:14px 0;border-bottom:1px solid #e9e9e9">
            <div style="font:600 12px/1 Inter,Arial,sans-serif;color:{colour};
                        letter-spacing:.08em;text-transform:uppercase">
              {r['site']} &middot; {r['state']}
            </div>
            <div style="font:600 17px/1.4 Georgia,serif;color:#111;margin:6px 0 4px">
              {r['title']}
            </div>
            <a href="{r['url']}" style="font:400 14px/1.4 Inter,Arial,sans-serif;color:#2563EB">
              {r['url']}
            </a>
            <div style="font:400 13px/1.5 Inter,Arial,sans-serif;color:#666;margin-top:6px">
              {r['meta']}
            </div>
          </td>
        </tr>"""

    note = ""
    if drafts:
        note = (f'<p style="font:400 14px/1.6 Inter,Arial,sans-serif;color:#8a5a00;'
                f'background:#fff8e6;padding:12px 14px;border-radius:8px">'
                f'{len(drafts)} post(s) are sitting as drafts. They will not go live '
                f'until you approve them.</p>')

    html = f"""<div style="max-width:620px;margin:0 auto;padding:24px">
      <div style="font:400 13px/1 Inter,Arial,sans-serif;color:#888">blog-bot &middot; {today}</div>
      <h1 style="font:600 24px/1.3 Georgia,serif;color:#111;margin:8px 0 18px">
        {len(results)} post(s) generated
      </h1>
      {note}
      <table style="width:100%;border-collapse:collapse">{rows}</table>
      <p style="font:400 12px/1.6 Inter,Arial,sans-serif;color:#999;margin-top:24px">
        Sent by the CI pipeline. Reply to nobody, this mailbox does not read.
      </p>
    </div>"""

    text = f"blog-bot {today} — {len(results)} post(s)\n\n" + "\n\n".join(
        f"{r['site']} [{r['state']}]\n{r['title']}\n{r['url']}" for r in results)
    return text, html


def send(results):
    user = os.environ["SMTP_USER"]
    pw = os.environ["SMTP_PASS"]
    text, html = render(results)

    msg = EmailMessage()
    msg["Subject"] = f"blog-bot: {len(results)} post(s) — {dt.date.today():%d %b}"
    msg["From"] = user
    msg["To"] = TO
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
        s.login(user, pw)
        s.send_message(msg)


if __name__ == "__main__":
    send([{"site": "repairrange", "title": "Test post", "state": "DRAFT — needs your approve",
           "url": "https://repairrange.io/blog/test.html", "meta": "Test."}])
