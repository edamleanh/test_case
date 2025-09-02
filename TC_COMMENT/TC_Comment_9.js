import { Selector } from 'testcafe';
import { BASE_URL } from '../store';

const usernameInput = Selector('#id_username');
const passwordInput = Selector('#id_password');
const logoImg = Selector('img[alt="DMOJ"][src="/static/icons/logo.svg"]');
const firstPostLink = Selector('a').withAttribute('href', '/post/1-first-post').withText('First Post');
const alertInfo = Selector('#new-comment .alert.alert-info').withText('You must solve at least one problem before your voice can be heard.');

fixture`Demo Login Test`
    .page`http://localhost:8000/accounts/login/`;

test('User can log in with valid credentials', async t => {
    await t
        .typeText(usernameInput, 'edamleanh')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .pressKey('enter')
        .click(logoImg)
        .click(firstPostLink)
        .expect(alertInfo.exists).ok('Should show the alert that you must solve at least one problem before commenting');
});

