import { chromium } from "@playwright/test";
import { mkdir } from "node:fs/promises";
import path from "node:path";

const baseUrl = process.env.FRONTEND_URL ?? "http://localhost:3000";
const outDir = path.resolve("../docs/screenshots");

async function main() {
  await mkdir(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });

  await page.goto(`${baseUrl}/login`);
  await page.screenshot({ path: path.join(outDir, "01_login.png"), fullPage: true });
  await page.fill('input:not([type="password"])', "employee01");
  await page.fill('input[type="password"]', "Password123!");
  await Promise.all([
    page.waitForURL("**/mfa"),
    page.click("button:has-text('SSOログイン')")
  ]);
  await page.screenshot({ path: path.join(outDir, "02_mfa.png"), fullPage: true });
  await Promise.all([
    page.waitForURL("**/dashboard"),
    page.click("button:has-text('承認')")
  ]);
  await page.waitForSelector("text=ログインユーザー");
  await page.screenshot({ path: path.join(outDir, "03_dashboard.png"), fullPage: true });

  const shots = [
    ["/admin/users", "04_users.png", "ユーザーID"],
    ["/admin/applications", "05_applications.png", "アプリケーション名"],
    ["/admin/policies", "06_policies.png", "ポリシー"],
    ["/admin/logs", "07_logs.png", "認証方式"],
    ["/vpn-login", "08_vpn_login.png", "VPNログイン"]
  ];
  for (const [url, name, text] of shots) {
    await page.goto(`${baseUrl}${url}`);
    await page.waitForLoadState("networkidle");
    await page.waitForSelector(`text=${text}`);
    await page.screenshot({ path: path.join(outDir, name), fullPage: true });
  }
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
