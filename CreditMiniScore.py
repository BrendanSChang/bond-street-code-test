class Loan:
    def __init__(self, amount, duration, payment_history):
        '''
        Constructor for a Loan.

        amount              The requested loan amount
        duration            A loan duration in months, where payments are expected on a monthly basis
        payment_history     The number of days overdue or paid in advance for each payment
        '''
        self.amount = amount
        self.duration = duration
        self.payment_history = payment_history

    def num_late_payments(self):
        return sum([1 if days_overdue > 0 else 0 for days_overdue in self.payment_history])

    def defaulted(self):
        for days_overdue in self.payment_history:
            if days_overdue >= 90:
                return True
        return False

class Business:
    # Constants
    MAX_CREDIT = 850
    MIN_CREDIT = 300

    def __init__(self, name, owner, assets, requested_amount, loan_history):
        '''
        Constructor for a Business.

        name                The name of the business
        owner               The owner of the business
        assets              The total assets of the business
        requested_amount    The total amount requested by for the loan
        loan_history        The business's loan history
        '''
        self.name = name
        self.owner = owner
        self.assets = assets
        self.requested_amount = requested_amount
        self.loan_history = loan_history

    def credit_mini_score(self):
        '''
        Build a credit mini score. This follows the same range for a standard FICO credit score, between 300 and 850.
        This method is extremely rudimentary, constructing the score using the following rules:

            1. Begin at a score of 600
            2. Remove up to 300 points for late payments on previous loans or previously defaulted loans
            3. Add 150 points for no late payments
            4. Add 100 points based on how much greater the business's assets are than the requested loan amount

        This method favors previous loan history more than any other factor. It also takes into account the business's
        current assets. Ideally, this method would also favor performances with more recent loans over loans farther
        in the past (potentially with a weighted distribution). Additionally, previous loans should be weighted on loan
        amount and advance payments should be favorably considered just as late payments are unfavorably considered.
        '''
        score = 600

        has_previously_defaulted = False
        total_late_payments = 0
        total_payments = 0
        for loan in self.loan_history:
            if loan.defaulted():
                has_previously_defaulted = True
                break
            total_late_payments += loan.num_late_payments()
            total_payments += loan.duration

        if total_late_payments > 0 or total_payments == 0:
            factor = 1
            if not has_previously_defaulted and total_payments > 0:
                factor = float(total_late_payments)/total_payments
    
            score -= (300 * factor)
        else:
            score += 150

        if self.assets > self.requested_amount:
            score += (100 * min(float(self.assets)/self.requested_amount, 5.)/5.)

        return int(score)

    def p_value(self):
        '''
        Let H_0 be the hypothesis that a small business defaults on a 3-month loan. In this context, defaulting is
        defined as any payment that is 90+ days overdue. Then, let C be the approximated credit score of the small
        business. This method attempts to derive the value P(H_0|C).

        This method models the distribution of default rates using the delinquency rates in the following presentation
        as a sample distribution.

            http://www.wvasf.org/presentation_pdfs/John_Meeks_-_WV_Asset_Building_Charleston_102811.pdf

        The approximated rate is linearly estimated within each credit score level. However, it would likely be more
        accurate to take more data into account and build a smoother distribution with parameter estimation.
        '''
        score = self.credit_mini_score()
        if score <= 499:
            # Instead of starting from the top percentage bound and working downwards, start from the bottom bound and
            # work upwards in this case. This ensures that the output of this method includes the entire 0-100% range.
            base = 87
            delta = -13
            score = 499 - score
            bound = 199
        elif score <= 549:
            base = 86
            delta = 15
            bound = 549
        elif score <= 599:
            base = 70
            delta = 19
            bound = 599
        elif score <= 649:
            base = 50
            delta = 19
            bound = 649
        elif score <= 699:
            base = 30
            delta = 15
            bound = 699
        elif score <= 749:
            base = 14
            delta = 9
            bound = 749
        elif score <= 799:
            base = 4
            delta = 2
            bound = 799
        else:
            base = 1
            delta = 1
            bound = 850

        default_rate = (base - (delta * (float(score)/bound)))/100
        return 1 - default_rate

    def __str__(self):
        return 'Business: {0}\nOwner: {1}\nRequested Amount: {2}\nCredit Score: {3}\np-value: {4}'.format(
            self.name, self.owner, self.requested_amount, self.credit_mini_score(), self.p_value())

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Approximate a rate of defaulting for a small business')
    parser.add_argument('--input', default='input.txt')
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as f:
            name = f.readline().strip()
            owner = f.readline().strip()
            assets = float(f.readline())
            requested_amount = float(f.readline())
            loan_history_lines = f.readlines()
            loan_history = []
            for i in xrange(0, len(loan_history_lines), 3):
                amount = float(loan_history_lines[i])
                duration = int(loan_history_lines[i+1])
                payment_history = [int(days_overdue) for days_overdue in loan_history_lines[i+2].split(',')]
                loan_history.append(Loan(amount, duration, payment_history))
        b = Business(name, owner, assets, requested_amount, loan_history)
        print b
    except IOError as e:
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
    except IndexError:
        print 'Input file format incorrect. Each Loan should have three lines.'
