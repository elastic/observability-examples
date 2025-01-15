const { faker } = require("@faker-js/faker");
const fs = require("fs");

const transactionYear = "2024";
const randomMonth = faker.number.int({ min: 1, max: 12 }).toString().padStart(2, 0);
const daysInMonth = new Date(transactionYear, randomMonth, 0).getDate();
const startDate = `${transactionYear}-${randomMonth}-01T00:00:00.000Z`;
const endDate = `${transactionYear}-${randomMonth}-${daysInMonth}T23:59:59Z`;

const genTransaction = (fixedIP, randomTimestamp) => {
    return {
        captureMethod: faker.helpers.arrayElement(["NOW", "LATER"]),
        amount: faker.number.int({ min: 10, max: 1200 }),
        currency: "USD",
        IPAddress: fixedIP || faker.internet.ipv4(),

        merchant: {
            merchantSoftware: {
                companyName: "Example Company",
                productName: faker.helpers.arrayElement([
                    "Tractor Beam Core", "Hyperdrive 8", "Anti Gravity Engine",
                    "Cloaking Shield", "Sandplanet Spice", "Galaxy Passport",
                ]),
                version: "4.2.0",
            },
            merchantCategoryCode: "1337",
        },
        paymentMethodType: {
            card: {
                accountNumber: faker.finance.creditCardNumber({ issuer: "visa" }),
                expiry: {
                    month: faker.number.int({ min: 1, max: 12 }).toString().padStart(2, 0),
                    year: faker.number.int({ min: 2025, max: 2030 }),
                },
                isBillPayment: faker.datatype.boolean(),
            },
        },
        initiatorType: "CARDHOLDER",
        accountOnFile: "NOT_STORED",
        isAmountFinal: true,
        timestamp: randomTimestamp || faker.date.between({ from: startDate, to: endDate }),
    };
};

const genTransactions = (numTransactions) => {
    const transactions = [];
    const fixedIP = faker.internet.ipv4();
    const randomNumber = faker.number.int({ min: 1, max: daysInMonth });
    const randomDay = randomNumber.toString().padStart(2, "0");
    const randomIndices = new Set();
    const randomMax = faker.number.int({ min: 30, max: 50 });

    while (randomIndices.size < randomMax) {
        randomIndices.add(Math.floor(Math.random() * numTransactions));
    }

    for (let i = 0; i < numTransactions; i++) {
        if (randomIndices.has(i)) {
            let randomDayStart = `${transactionYear}-${randomMonth}-${randomDay}T00:00:00.000Z`;
            let randomDayEnd = `${transactionYear}-${randomMonth}-${randomDay}T23:59:59Z`;
            let randomTimestamp = faker.date.between({ from: randomDayStart, to: randomDayEnd });
            transactions.push(genTransaction(fixedIP, randomTimestamp));
        } else {
            transactions.push(genTransaction());
        }
    }
    return transactions;
};

let dataObj = genTransactions(1000);

const ndjson = dataObj.map(JSON.stringify).join("\n");
fs.writeFileSync("transactions.ndjson", ndjson, "utf8");
